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
            x=600,
            y=300,
            img="waterfall.png",
            animation="fall",
            animation_speed=12,
            sound=["waterfall.ogg"],
            sound_autoplay=True,
            sound_loop=True,
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
        for k, v in args.items():
            setattr(self, k, v)
        self.changed = True

    def __dump__(self):
        return self.dumpable


class Users(object):

    def __init__(self):
        self.users = {}

    def create(self, id, ws):
        user = User(ws)
        self.users[id] = user
        return user

    # def send_all(self, id):
    #     self.users[id].send_map(MAP)

    def connect(self, id, ws):
        user = self.create(id, ws)
        user.send_map(MAP)
        MAP.add(user)
        return user

    def disconnect(self, id):
        user = self.users[id]
        self.users[id] = None
        MAP.remove(user)
        del user.ws


class User(MapElement):

    def __init__(self, ws):
        super(User, self).__init__(x=10, y=10, img="bunny.png")
        self.ws = ws

    def receive(self):
        return self.ws.receive()

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
USERS = Users()


# @ws.route('/websocket')
@sockets.route('/websocket')
def communicator(ws):
    print("CONECTANDO", ws)
    id = len(USERS.users)
    user = USERS.connect(id, ws)
    print("CONECTADO", ws)
    user.listen()
    USERS.disconnect(id)

# if __name__ == '__main__':
#     if GEVENT:
#         app.run(debug=True, gevent=100)
#     else:
#         app.run(debug=True, threads=16)
