#!/usr/bin/env python
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
users = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


def send_data():
    for user in users:
        print("================", users)
        for i in map:
            print("~~~~~~~~~~~~~~~~~~~~", user)
            user.send("%s,%s,%s" % i)


# @ws.route('/websocket')
@sockets.route('/websocket')
def communicator(ws):
    print("=-----------------------", ws)
    users.append(ws)
    print("AAAAAAAAAAAAAAAAAAAAA")
    send_data()
    print("BBBBBBBBBBB")
    while True:
        print("oAAAAAAAAAAAAAAAAAAAA")
        msg = ws.receive()
        print(msg)
        if msg is not None:
            x, y = msg.decode("utf8").split(',')
            id = len(map)
            map.append((id, x, y))
            send_data()
        else:
            break
    users.remove(ws)
    del ws

# if __name__ == '__main__':
#     if GEVENT:
#         app.run(debug=True, gevent=100)
#     else:
#         app.run(debug=True, threads=16)
