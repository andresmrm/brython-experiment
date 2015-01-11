import json

from browser import window
from javascript import JSConstructor

from amoamo.sound import SoundManager


SM = SoundManager("/static/sounds/")
window.SM = SM


class Element(object):

    def __init__(self, sprite, sound=None):
        self.sprite = sprite
        self.sound = sound


class Game(object):

    def __init__(self):
        window.console.log("game-init")
        Game = JSConstructor(window.Phaser.Game)
        window.br_preload = self.preload
        window.br_create = self.create
        window.br_update = self.update
        window.br_render = self.render
        window.game = Game(
            800,
            600,
            window.Phaser.AUTO,
            'canvas-anchor',
            window.stater)
        self.game = window.game
        self.elements = []
        window.console.log("game-init-fim")

    @staticmethod
    def preload():
        window.console.log("game-preload")
        window.game.load.image('bunny', '/static/img/bunny.png')
        window.game.load.image('grass', '/static/img/grass.png')
        window.game.load.image('tree', '/static/img/tree1.png')
        window.game.load.spritesheet(
            'waterfall.png',
            '/static/img/waterfall1.png',
            96,
            173)
        window.console.log("game-preload-fim")
        window.game.time.advancedTiming = True

    @staticmethod
    def create():
        x = y = 2000

        # Fix 0 beeing converted to null by Brython
        arcade = window.Phaser.Physics.ARCADE
        if not arcade:
            arcade = 0

        window.console.log("game-create")
        window.game.physics.startSystem(arcade)
        window.game.world.setBounds(0, 0, x, y)

        window.game.stage.backgroundColor = '#2d2d2d'
        window.game.add.tileSprite(0, 0, x, y, 'grass')

        window.sprite = window.game.add.sprite(32, 200, 'bunny')
        window.sprite.name = 'bunny-dude'
        window.game.camera.follow(window.sprite)
        # window.game.camera.setPosition(1000,1000)

        window.game.physics.enable(window.sprite, arcade)

        window.group = window.game.add.group()
        window.group.enableBody = True
        window.group.physicsBodyType = arcade

        # for i in range(50):
        #     c = window.group.create(
        #         window.game.rnd.integerInRange(
        #             0, x), window.game.rnd.integerInRange(
        #             0, y), 'tree')
        #     c.name = 'tree' + str(i)
        #     c.body.immovable = True

        # for (var i = 0; i < 20; i++)
        # {
        #     //  Here we'll create some chillis which the
        #     player can pick-up. They are still part of the same Group.

        #     var c = group.create(game.rnd.integerInRange(100, 770), \
        #     game.rnd.integerInRange(0, 570), 'veggies', 17);

        #     c.name = 'chilli' + i;
        #     c.body.immovable = true;
        # }
        SM.load('forest', ['forest.ogg'], loop=True, autoplay=True)

        window.cursors = window.game.input.keyboard.createCursorKeys()
        window.console.log("game-create-fim")

    @staticmethod
    def update():
        # window.console.log("game-update")

        window.game.physics.arcade.collide(
            window.sprite,
            window.group,
            # Game.collisionHandler,
            None,
            None,
            Game)
        window.game.physics.arcade.collide(window.group, window.group)

        window.sprite.body.velocity.x = 0
        window.sprite.body.velocity.y = 0
        x = window.sprite.body.x
        y = window.sprite.body.y

        SM.set_listener_pos(x, y)

        if window.cursors.left.isDown:
            window.sprite.body.velocity.x = -200
        elif window.cursors.right.isDown:
            window.sprite.body.velocity.x = 200

        if window.cursors.up.isDown:
            window.sprite.body.velocity.y = -200
        elif window.cursors.down.isDown:
            window.sprite.body.velocity.y = 200
        # window.console.log("game-update-fim")
        window.game.world.wrap(window.sprite, 0, True)

    @staticmethod
    def render():
        # if window.game.time.fps:
        window.game.debug.text(window.game.time.fps, 2, 14, "#00ff00")

    @staticmethod
    def collisionHandler(player, obj):
        window.console.log(player)
        window.console.log(obj)

    def process_msg(self, evt):
        msg = json.loads(evt.data)
        command = msg[0]
        list_args = msg[1]
        window.console.log(msg)
        method = getattr(self, command)
        window.console.log(method)
        for args in list_args:
            method(args)

    def add_element(self, args):
        window.console.log("add_element")
        window.console.log(args)
        visual_element = sound_element = None
        # if has an image
        img = args.get('img')
        if img:
            x = args.get('x')
            y = args.get('y')
            visual_element = window.game.add.sprite(x, y, img)
            # if has an animation
            animation = args.get('animation')
            if animation:
                visual_element.animations.add(animation)
                animation_speed = args.get('animation_speed', 10)
                visual_element.animations.play(animation, animation_speed, True)

        # if has a sound
        sound = args.get('sound')
        window.console.log(sound)
        if sound:
            x = args.get('x')
            y = args.get('y')
            z = args.get('z')
            sound_element = SM.load(
                sound,
                loop=args.get('sound_loop', False),
                autoplay=args.get('sound_autoplay', False),
                x=x,
                y=y,
                z=z,
            )
            window.som = sound_element

        self.elements.append(Element(visual_element, sound_element))
        window.console.log("add_element-fim")
