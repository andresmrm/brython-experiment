from browser import alert, websocket


# PyFlakes, why don't you STFU?!
if False:
    __BRYTHON__ = None


class WebSocket(object):

    def __init__(self, host, on_message):
        self.host = host
        self.ws = None
        self.on_message = on_message
        self.open_websocket()

    def open_websocket(self):
        if not __BRYTHON__.has_websocket:
            alert("WebSocket is not supported by your browser")
            return
        # open a web socket
        self.ws = websocket.websocket(self.host)
        self.ws.bind('open', self.on_open)
        self.ws.bind('message', self.on_message)
        self.ws.bind('close', self.on_close)

    def close_connection(self):
        self.ws.close()

    def send(self, data):
        self.ws.send(data)

    def on_open(self, evt):
        # print(self, evt)
        alert("Connection is OPEN!")
        pass

    # def on_message(self, evt):
        # # message reeived from server
        # # alert("Message received : %s" % evt.data)
        # alert(evt.data)

    def on_close(self, evt):
        # websocket is closed
        alert("Connection is closed")
