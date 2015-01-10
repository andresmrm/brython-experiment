# from browser import document as doc
from browser import alert, websocket, window
from javascript import JSConstructor, JSObject


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

    def on_message(self, evt, a):
        # message reeived from server
        # alert("Message received : %s" % evt.data)
        id, x, y = [int(i) for i in evt.data.split(',')]
        if id not in bunnies:
            bunny = GAME.add_element("/static/img/bunny.png", x, y)
            bunnies[id] = bunny

    def on_close(evt):
        # websocket is closed
        alert("Connection is closed")

# ws_addr = "ws://" + window.location.host + "/websocket"
# WS = WebSocket(ws_addr)

bunnies = {}


class Game(object):

    def __init__(self):
        window.console.log("game-init")
        Game = JSConstructor(window.Phaser.Game)
        window.br_preload = self.preload
        window.br_create = self.create
        window.br_update = self.update
        window.game = Game(800, 600, window.Phaser.AUTO, 'canvas-anchor', window.stater)
        self.game = window.game
        window.console.log("game-init-fim")

    @staticmethod
    def preload():
        window.console.log("game-preload")
        window.game.load.image('bunny', '/static/img/bunny.png')
        window.game.load.image('grass', '/static/img/grass.png')
        window.game.load.image('tree', '/static/img/tree1.png')
        window.game.load.spritesheet('waterfall', '/static/img/waterfall1.png', 96, 173)
        window.console.log("game-preload-fim")

    @staticmethod
    def create():
        x = y = 2000

        # Fix 0 beeing converted to null by Brython
        arcade = window.Phaser.Physics.ARCADE
        if not arcade:
            arcade = 0

        window.console.log("game-create")
        window.game.physics.startSystem(arcade)
        window.game.world.setBounds(0, 0, x, y);

        window.game.stage.backgroundColor = '#2d2d2d'
        window.game.add.tileSprite(0, 0, x, y, 'grass');

        window.sprite = window.game.add.sprite(32, 200, 'bunny')
        window.sprite.name = 'bunny-dude'
        window.game.camera.follow(window.sprite)
        # window.game.camera.setPosition(1000,1000)

        window.game.physics.enable(window.sprite, arcade)

        window.group = window.game.add.group()
        window.group.enableBody = True
        window.group.physicsBodyType = arcade

        for i in range(50):
            c = window.group.create(window.game.rnd.integerInRange(0, x), window.game.rnd.integerInRange(0, y), 'tree')
            c.name = 'tree' + str(i)
            c.body.immovable = True

        # for (var i = 0; i < 50; i++)
        # {
            # var c = group.create(game.rnd.integerInRange(100, 770), game.rnd.integerInRange(0, 570), 'veggies', game.rnd.integerInRange(0, 35));
            # c.name = 'veg' + i;
            # c.body.immovable = true;
        # }

        # for (var i = 0; i < 20; i++)
        # {
            # //  Here we'll create some chillis which the player can pick-up. They are still part of the same Group.
            # var c = group.create(game.rnd.integerInRange(100, 770), game.rnd.integerInRange(0, 570), 'veggies', 17);
            # c.name = 'chilli' + i;
            # c.body.immovable = true;
        # }

        waterfall = window.game.add.sprite(300, 200, 'waterfall')
        waterfall.animations.add('fall')
        waterfall.animations.play('fall', 12, True)

        window.cursors = window.game.input.keyboard.createCursorKeys()
        window.console.log("game-create-fim")


    @staticmethod
    def update():
        # window.console.log("game-update")

        window.game.physics.arcade.collide(window.sprite, window.group, None, None, Game)
        window.game.physics.arcade.collide(window.group, window.group)

        window.sprite.body.velocity.x = 0
        window.sprite.body.velocity.y = 0

        if window.cursors.left.isDown:
            window.sprite.body.velocity.x = -200
        elif window.cursors.right.isDown:
            window.sprite.body.velocity.x = 200

        if window.cursors.up.isDown:
            window.sprite.body.velocity.y = -200
        elif window.cursors.down.isDown:
            window.sprite.body.velocity.y = 200
        # window.console.log("game-update-fim")
        window.game.world.wrap(window.sprite, 0, True);

    def collisionHandler(self):
        pass

# function collisionHandler (player, veg) {

#     //  If the player collides with the chillis then they get eaten :)
#     //  The chilli frame ID is 17

#     if (veg.frame == 17)
#     {
#         veg.kill();
#     }

# }


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


window.console.log("1")
GAME = Game()
window.console.log("2")
