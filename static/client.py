from browser import document as doc
from browser import alert, websocket, window
from javascript import JSConstructor


# PyFlakes, why don't you STFU?!
if False:
    __BRYTHON__ = None


def on_open(evt):
    doc['send'].disabled = False
    doc['close'].disabled = False
    doc['open'].disabled = True


def on_message(evt):
    # message reeived from server
    alert("Message received : %s" % evt.data)


def on_close(evt):
    # websocket is closed
    alert("Connection is closed")
    doc['open'].disabled = False
    doc['close'].disabled = True
    doc['send'].disabled = True

ws = None


def _open(ev):
    if not __BRYTHON__.has_websocket:
        alert("WebSocket is not supported by your browser")
        return
    global ws
    # open a web socket
    # ws = websocket.websocket("wss://echo.websocket.org")
    host = "ws://127.0.0.1:8080/websocket"
    ws = websocket.websocket(host)
    # bind functions to web socket events
    ws.bind('open', on_open)
    ws.bind('message', on_message)
    ws.bind('close', on_close)


def send(ev):
    data = doc["zone"].value
    if data:
        ws.send(data)


def close_connection(ev):
    ws.close()
    doc['open'].disabled = False

doc['open'].bind('click', _open)
doc['send'].bind('click', send)
doc['close'].bind('click', close_connection)


def initilize_pixi():
    # create an new instance of a pixi stage
    Stage = JSConstructor(window.PIXI.Stage)
    stage = Stage(0x66FF99, True)

    # create a renderer instance
    renderer = window.PIXI.autoDetectRenderer(800, 600)

    # add the renderer view element to the DOM
    doc['body'] <= renderer.view

    bunny = add_element(stage, "/static/img/bunny.png", 20, 20)
    bunny.setInteractive(True)

    def f(x):
        print(x)

    bunny.mouseover = f

    def animate():
        window.requestAnimFrame(animate)
        # just for fun, lets rotate mr rabbit a little
        bunny.rotation += 0.1
        # render the stage
        renderer.render(stage)

    window.requestAnimFrame(animate)


def add_element(stage, texture_image, x, y):
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
    stage.addChild(sprite)
    return sprite

initilize_pixi()
