#!/usr/bin/env python
import json
from collections import OrderedDict

import gevent
from gevent.queue import Queue

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
# try:
#     from flask.ext.uwsgi_websocket import GeventWebSocket
#     ws = GeventWebSocket(app)
#     GEVENT = True
# except:
#     from flask.ext.uwsgi_websocket import WebSocket
#     ws = WebSocket(app)
#     GEVENT = False

from flask_sockets import Sockets
sockets = Sockets(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


class MyEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dump__()


class Map(object):

    def __init__(self):
        self.elements = []
        self.modified = OrderedDict()
        self.daytime = 12

    def run_daytime(self):
        """Thread that take care of the time of the day"""
        while True:
            gevent.sleep(60)
            self.daytime += 1
            if self.daytime >= 24:
                self.daytime = 0
            PLAYERS.broadcast_command("set_daytime", [(self.daytime,)])
            print("TIME: ", self.daytime)

    def add(self, element):
        self.elements.append(element)

    def remove(self, element):
        self.elements.remove(element)

    def add_modified(self, element):
        """Add an element to the modified list, so it can be updated to other
        players"""
        self.modified[element] = True

    def remove_modified(self, element):
        """Remove an element from the modified list"""
        self.modified.pop(element)

    def get_modified(self):
        """Pops elements from list and returns them"""
        try:
            while True:
                element = self.modified.popitem(last=False)
                print("----------", element)
                yield element[0]
        except KeyError:
            pass

    def __dump__(self):
        return self.elements


class MapElement(object):

    def __init__(self, **args):
        # Everything that is passed in args will be dumped via network
        self.dumpable = args.keys()
        if 'id' not in args:
            # TODO no random...
            import random
            id = random.randint(0, 30000)
            args['id'] = id
        for k, v in args.items():
            setattr(self, k, v)

        self.set_modified()

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.set_modified()

    def set_modified(self):
        MAP.add_modified(self)

    def __dump__(self):
        dump = {}
        for k, v in self.__dict__.items():
            if k in self.dumpable:
                dump[k] = v
        return (dump,)


class Players(object):

    def __init__(self):
        self.players = {}
        gevent.spawn(self.update_players)
        gevent.spawn(MAP.run_daytime)
        self.commands_queue = Queue()

    # def create(self, id, ws):
    #     self.players[id] = player
    #     return player

    # def send_all(self, id):
    #     self.players[id].send_map(MAP)

    def connect(self, ws):
        new_player = Player(ws)
        name = new_player.wait_login()
        self.players[name] = new_player
        new_player.create_avatar(MAP)
        # Send world for new player
        self.add_command(new_player, 'add_element', MAP)
        self.add_command(new_player, 'set_daytime', [(MAP.daytime, True)])
        # Send new player for other players
        for player in self.players.values():
            if player is not new_player:
                self.add_command(player, 'add_element', [new_player.avatar])

        return new_player

    def disconnect(self, name):
        player = self.players[name]
        self.players[name] = None
        player.remove_avatar(MAP)
        del player.ws

    def add_command(self, player, command, args):
        # Adds a command to the command queue
        self.commands_queue.put((player, command, args))

    def broadcast_command(self, command, args):
        for player in self.players.values():
            self.add_command(player, command, args)

    def update_players(self):
        while True:
            gevent.sleep(.1)
            msgs = {}
            # WATER.set_modified()
            for element in MAP.get_modified():
                print(element.id)
                for player in self.players.values():
                    # Player may not have avatar yet...
                    print("P:", player)
                    try:
                        avatar = player.avatar
                    except AttributeError:
                        pass
                    if element is not avatar:
                        # add element to be updated to each player
                        # a dict is used to avoid repetition of elements
                        print("N")
                        elements = msgs.get(player, {})
                        elements[element] = True
                        msgs[player] = elements

            print(msgs)

            for player, elements in msgs.items():
                args = []
                for element in elements:
                    # TODO update more than pos?
                    arg = {
                        "id": element.id,
                        "x": element.x,
                        "y": element.y,
                    }
                    args.append(arg)

                print("SEND", player, args)
                # player were None once. maybe a paralelism problem!!!
                if player:
                    player.send_command("update_element", args)

            # Other commands
            self.commands_queue.put(StopIteration)
            for pack in self.commands_queue:
                player = pack[0]
                command = pack[1]
                args = pack[2]
                # player were None once. maybe a paralelism problem!!!
                if player:
                    player.send_command(command, args)


class Player(object):

    def __init__(self, ws):
        self.ws = ws

    def receive(self):
        return self.ws.receive()

    def wait_login(self):
        data = self.receive()
        msg = json.loads(data)
        if msg[0] == 'login':
            self.name = str(msg[1])
            return self.name
        else:
            raise 'Waiting "login", but got: ' + msg

    def create_avatar(self, map):
        self.avatar = MapElement(
            id="avatar_" + self.name,
            x=10,
            y=10,
            img="bunny.png")
        map.add(self.avatar)
        return self.avatar

    def remove_avatar(self, map):
        map.remove(self.avatar)

    # def send_map(self, map):
        # self.send_command('add_element', map)

    def send_command(self, command, data):
        dump = json.dumps([command, data], cls=MyEncoder)
        self.ws.send(dump)

    def listen(self):
        while True:
            data = self.receive()
            print(data)
            if data is not None:
                msg = json.loads(data)
                if msg[0] == 'p':
                    x, y = msg[1]
                    self.avatar.set_pos(x, y)
                if msg[0] == 'c':
                    x, y, element = msg[1]
                    me = MapElement(
                        x=x,
                        y=y,
                        img="tree2.png",
                    )
                    MAP.add(me)
                    for player in PLAYERS.players.values():
                        PLAYERS.add_command(player, 'add_element', [me])
            else:
                break


MAP = Map()
PLAYERS = Players()

me = MapElement(
    x=300,
    y=0,
    img="waterfall.png",
    animation="fall",
    animation_speed=12,
    sound=["waterfall.ogg"],
    sound_autoplay=True,
    sound_loop=True,
)
MAP.add(me)
WATER = me
me = MapElement(
    id="sound_day",
    sound=["forest.ogg"],
    # sound_autoplay=True,
    sound_loop=True,
)
MAP.add(me)
me = MapElement(
    id="sound_night",
    sound=["night.ogg"],
    # sound_autoplay=True,
    sound_loop=True,
)
MAP.add(me)
me = MapElement(
    x=400,
    y=200,
    img="tree2.png",
)
MAP.add(me)


# @ws.route('/websocket')
@sockets.route('/websocket')
def communicator(ws):
    print("New player connecting!", ws)
    player = PLAYERS.connect(ws)
    print("Loged in: ", player.name)
    player.listen()
    PLAYERS.disconnect(player.name)
    print("Player disconnected: ", player.name)

# if __name__ == '__main__':
#     if GEVENT:
#         app.run(debug=True, gevent=100)
#     else:
#         app.run(debug=True, threads=16)
