from browser import document as doc
from browser import alert, websocket, window
from javascript import JSConstructor


# PyFlakes, why don't you STFU?!
if False:
    __BRYTHON__ = None


class WebSocket(object):

    def __init__(self, host):
        self.host = host
        self.ws = None
        self.open_websocket()

    def open_websocket(self, ev):
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
        pass

    def on_message(self, evt):
        # message reeived from server
        # alert("Message received : %s" % evt.data)
        x, y = [int(i) for i in evt.data.split(',')]
        bunny = DRAWER.add_element("/static/img/bunny.png", x, y)
        bunnies.append(bunny)

    def on_close(evt):
        # websocket is closed
        alert("Connection is closed")


WS = WebSocket("ws://127.0.0.1:8080/websocket")

bunnies = []


class Drawer(object):

    def __init__(self):
        self.init_pixi()

    def init_pixi(self):
        # create an new instance of a pixi stage
        Stage = JSConstructor(window.PIXI.Stage)
        self.stage = Stage(0x66FF99, True)

        # create a renderer instance
        self.renderer = window.PIXI.autoDetectRenderer(800, 600)

        # add the renderer view element to the DOM
        doc['body'] <= self.renderer.view

        grass = self.add_element("/static/img/grass.png", 200, 200)
        grass.setInteractive(True)

        def g(evt):
            x = evt['originalEvent']['clientX']
            y = evt['originalEvent']['clientY']
            WS.send((x, y))

        grass.mousedown = g
        texture = window.PIXI.Texture.fromImage("/static/img/bunny.png")

        def animate():
            window.requestAnimFrame(animate)
            # just for fun, lets rotate mr rabbit a little
            for bunny in bunnies:
                bunny.rotation += 0.1
            # render the stage
            self.renderer.render(self.stage)

        window.requestAnimFrame(animate)

    def add_element(self, texture_image, x, y):
        # create a texture from an image path
        texture = window.PIXI.Texture.fromImage(texture_image)
        # create a new Sprite using the texture
        Sprite = JSConstructor(window.PIXI.Sprite)
        sprite = Sprite(texture)
        # center the sprites anchor point
        sprite.anchor.x = 0.5
        sprite.anchor.y = 0.5
        # move the sprite t the center of the screen
        sprite.position.x = x
        sprite.position.y = y
        self.stage.addChild(sprite)
        return sprite


DRAWER = Drawer()
