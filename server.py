#!/usr/bin/env python
import json

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


map = []


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
        me = MapElement(
            x=300,
            y=200,
            img="waterfall.png",
            animation="fall",
            animation_speed=12,
            sound=["waterfall.ogg"],
            sound_autoplay=True,
            sound_loop=True,
        )
        self.add(me)
        me = MapElement(
            sound=["forest.ogg"],
            sound_autoplay=True,
            sound_loop=True,
        )
        self.add(me)
        me = MapElement(
            x=400,
            y=200,
            img="tree.png",
        )
        self.add(me)

    def add(self, element):
        self.elements.append(element)

    def remove(self, element):
        self.elements.remove(element)

    def __dump__(self):
        return self.elements


class MapElement(object):

    def __init__(self, **args):
        # Everything that is passed in args will be dumped for network
        self.dumpable = args
        if 'id' not in args:
            # TODO no random...
            import random
            id = random.randint(0, 30000)
            args['id'] = id
        for k, v in args.items():
            setattr(self, k, v)

        self.changed = True

    def __dump__(self):
        return self.dumpable


class Players(object):

    def __init__(self):
        self.players = {}

    # def create(self, id, ws):
    #     self.players[id] = player
    #     return player

    # def send_all(self, id):
    #     self.players[id].send_map(MAP)

    def connect(self, ws):
        player = Player(ws)
        name = player.wait_login()
        self.players[name] = player
        player.create_avatar(MAP)
        player.send_map(MAP)
        return player

    def disconnect(self, name):
        player = self.players[name]
        self.players[name] = None
        player.remove_avatar(MAP)
        del player.ws


class Player(MapElement):

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

    def send_map(self, map):
        self.send_data('add_element', map)

    def send_data(self, command, data):
        dump = json.dumps([command, data], cls=MyEncoder)
        self.ws.send(dump)

    def listen(self):
        while True:
            msg = self.receive()
            print(msg)
            if msg is not None:
                x, y = msg.decode("utf8").split(',')
                id = len(map)
                map.append((id, x, y))
                self.send_data()
            else:
                break


MAP = Map()
PLAYERS = Players()


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
