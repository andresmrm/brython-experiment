#!/usr/bin/env python
from flask import Flask, render_template, send_from_directory
from flask.ext.uwsgi_websocket import WebSocket


app = Flask(__name__)
ws = WebSocket(app)


map = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@ws.route('/websocket')
def echo(ws):
    while True:
        msg = ws.receive()
        print(msg)
        if msg is not None:
            x, y = msg.decode("utf8").split(',')
            map.append((x, y))
            print(map)
            ws.send(msg.upper())
        else:
            return

if __name__ == '__main__':
    app.run(debug=True, threads=16)
