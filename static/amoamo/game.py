import json

from browser import window
from javascript import JSConstructor, JSObject

from amoamo.sound import SoundManager


SM = SoundManager("/static/sounds/")
window.SM = SM


def set_filter(sprite):
    # Dark magic to allow setting filter (why?!)
    # window.console.log(sprite)
    array = JSObject(JSConstructor(window.Array)())
    array.push(window.filter)
    sprite.filters = array


class Element(object):

    def __init__(self, sprite, sound=None):
        # self.going_to = None
        self.sprite = sprite
        self.sound = sound
        self.moving = None

    def set_pos(self, x, y):
        self.sprite.x = x
        self.sprite.y = y
        # TODO set sonud pos
        # if self.sound:
        #     self.sound.

    def move_to_pos(self, x, y):
        # self.going_to = (x, y)
        # window.game.physics.arcade.moveToXY(self.sprite, x, y, 200, 100)
        # self.GAME.moving.append(self)
        self.sprite.moves = False
        if self.moving:
            self.moving.stop(True)
        window.sprite = self.sprite
        self.moving = window.game.add.tween(self.sprite)
        self.moving.to({"x": x, "y": y}, 200,
                       window.Phaser.Easing.Default, True)


class Game(object):

    def __init__(self):
        window.console.log("game-init")

        window.avatar = None

        # player name
        self.name = None

        # special commands to send to server
        self.send_queue = []

        # elements moving and that need

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
        self.elements = {}

        # Day/Night light colors
        self.amb_light = {
            "noon": {"r": 1.0, "rs": 0.0, "g": 1.0, "gs": 0.0,
                     "b": 1.0, "bs": 0.0},
            "dusk": {"r": 0.9, "rs": 0.15, "g": 0.8, "gs": 0.0,
                     "b": 0.8, "bs": 0.0},
            "dawn": {"r": 0.9, "rs": 0.10, "g": 0.85, "gs": 0.05,
                     "b": 0.8, "bs": 0.0},
            "night": {"r": 0.3, "rs": 0.0, "g": 0.5, "gs": 0.0,
                      "b": 0.6, "bs": 0.15},
        }
        # Ambient light tween
        self.daynight = None
        # Number with the current time
        self.daytime = None

        window.console.log("game-init-fim")

    @staticmethod
    def preload():
        window.console.log("game-preload")

        window.game.load.script('filter', '/static/js/filter.js?982dk9823891')

        window.game.load.image('bunny.png', '/static/img/bunny.png')
        window.game.load.image('grass', '/static/img/grass2.png')
        # window.game.load.image('grass', '/static/img/grass.png')
        window.game.load.image('tree.png', '/static/img/tree.png')
        window.game.load.image('tree2.png', '/static/img/tree2.png')
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

        # window.game.stage.backgroundColor = '#2c8b2a'
        window.tile = window.game.add.tileSprite(0, 0, x, y, 'grass')

        # window.sprite = window.game.add.sprite(32, 200, 'bunny')
        # window.sprite.name = 'bunny-dude'
        # window.game.camera.follow(window.sprite)
        # window.game.camera.setPosition(1000,1000)

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

        window.cursors = window.game.input.keyboard.createCursorKeys()

        # Getting code is bugged...
        code = window.Phaser.Keyboard.C
        if not code:
            # key C
            code = 67
        key1 = window.game.input.keyboard.addKey(code)
        key1.onDown.add(window.GAME.test_create)

        window.filter = window.game.add.filter('DayLight')
        set_filter(window.tile)

        window.GAME.login()

        window.console.log("game-create-fim")

    @staticmethod
    def update():
        # window.console.log("game-update")
        if window.avatar:
            window.game.physics.arcade.collide(
                window.avatar,
                window.group,
                # Game.collisionHandler,
                None,
                None,
                Game)
            window.game.physics.arcade.collide(window.group, window.group)

            window.avatar.body.velocity.x = 0
            window.avatar.body.velocity.y = 0
            x = window.avatar.body.x
            y = window.avatar.body.y

            SM.set_listener_pos(x, y)

            window.avatar.moved = False
            if window.cursors.left.isDown:
                window.avatar.body.velocity.x = -200
                window.avatar.moved = True
            elif window.cursors.right.isDown:
                window.avatar.body.velocity.x = 200
                window.avatar.moved = True

            if window.cursors.up.isDown:
                window.avatar.body.velocity.y = -200
                window.avatar.moved = True
            elif window.cursors.down.isDown:
                window.avatar.body.velocity.y = 200
                window.avatar.moved = True

            if window.game.input.mousePointer.isDown:
                window.game.physics.arcade.moveToPointer(window.avatar, 200)
                window.avatar.moved = True

            # window.console.log("game-update-fim")
            window.game.world.wrap(window.avatar, 0, True)

    @staticmethod
    def render():
        # if window.game.time.fps:
        window.game.debug.text(window.game.time.fps, 2, 14, "#00ff00")

    @staticmethod
    def collisionHandler(player, obj):
        window.console.log(player)
        window.console.log(obj)

    def slow_update(self):
        # send in a regular period
        if window.avatar.moved:
            window.GAME.send_pos()
        while self.send_queue:
            c, x, y, element = self.send_queue.pop(0)
            self.send_new_element(x, y, element)

    def send_pos(self):
        """Send the position of this player"""
        x = int(window.avatar.body.x)
        y = int(window.avatar.body.y)
        data = json.dumps(["p", (x, y)])
        window.WS.send(data)

    def send_new_element(self, x, y, element):
        """Send an element created by this player"""
        data = json.dumps(["c", (x, y, element)])
        window.WS.send(data)

    @staticmethod
    def test_create(ev):
        window.console.log("CREATE")
        window.console.log(ev)
        x = int(window.avatar.body.x)
        y = int(window.avatar.body.y)
        element = "1"
        window.GAME.create_new_element(x, y, element)
        window.console.log("CREATE-fim")

    def create_new_element(self, x, y, element):
        self.send_queue.append(('c', x, y, element))

    def process_msg(self, evt):
        """Process incoming messages"""
        msg = json.loads(evt.data)
        command = msg[0]
        list_args = msg[1]
        # window.console.log(msg)
        method = getattr(self, command)
        print("list_arg")
        window.console.log(list_args)
        if list_args:
            for args in list_args:
                print("arg")
                window.console.log(args)
                method(*args)
        else:
            method()

    def slowly_switch_sounds(self, ida, idb, duration):
        # ID of the element that has the sound starting
        # ID of the element that has the sound stopping
        # duration (in milisecs) of the start
        sound = self.elements.get(ida)
        if sound:
            sound.sound.play()
            sound.sound.fade(0, 1, duration)

        sound = self.elements.get(idb)
        if sound:
            # TODO this seems not to work...
            def mini_stop():
                sound.sound.stop()
                print("STOP")
                window.console.log(sound)
            sound.sound.fade(1, 0, duration)
            sound.sound.faded = mini_stop

    def set_daytime(self, time, force=False):
        window.console.log(time)
        window.console.log(force)
        self.daytime = time

        if not self.daynight:
            window.GAME.daynight = window.game.add.tween(window.filter)
        else:
            # Stops possible old tween (who knows...)
            try:
                window.GAME.daynight.stop(True)
            except:
                pass

        s = 30
        if time == 6:
            self.dawn(s)
        elif time == 7:
            self.noon(s)
        elif time == 18:
            self.dusk(s)
        elif time == 19:
            self.night(s)

        # Forces an effect (usefull for the game start)
        if force:
            if time > 7 and time < 18:
                self.noon(1)
                sound = self.elements.get("sound_day")
                if sound:
                    sound.sound.play()
            elif time > 19 or time < 6:
                self.night(1)
                sound = self.elements.get("sound_night")
                if sound:
                    sound.sound.play()

    def dawn(self, duration, transition=window.Phaser.Easing.Default):
        """Starts the light and sounds for dawn
        Transition duration in seconds
        Trasition type function"""
        # colors, transition time, trasition type, autostart, wait before
        self.daynight.to(self.amb_light["dawn"], 1000 * duration,
                         transition, True)
        self.slowly_switch_sounds("sound_day", "sound_night", 1000 * duration)
        print("DAWN")

    def noon(self, duration, transition=window.Phaser.Easing.Default):
        """Starts the light and sounds for noon.
        Transition duration in seconds
        Trasition type function"""
        # colors, transition time, trasition type, autostart, wait before
        self.daynight.to(self.amb_light["noon"], 1000 * duration,
                         transition, True)
        print("NOON")

    def night(self, duration, transition=window.Phaser.Easing.Default):
        """Starts the light and sounds for night.
        Transition duration in seconds
        Trasition type function"""
        # colors, transition time, trasition type, autostart, wait before
        self.daynight.to(self.amb_light["night"], 1000 * duration,
                         transition, True)
        print("NIGHT")

    def dusk(self, duration, transition=window.Phaser.Easing.Default):
        """Starts the light and sounds for night.
        Transition duration in seconds
        Trasition type function"""
        # colors, transition time, trasition type, autostart, wait before
        self.daynight.to(self.amb_light["dusk"], 1000 * duration,
                         transition, True)
        self.slowly_switch_sounds("sound_night", "sound_day", 1000 * duration)
        print("DUSK")

    def login(self):
        window.console.log("LOGIN!")
        self.name = str(window.Math.floor(window.Math.random()*100))
        data = json.dumps(["login", self.name])
        window.WS.send(data)
        window.console.log("LOGED!")

    def open(self, evt):
        window.console.log("OPEN!!!!!!!!!!!")

    def close(self, evt):
        window.console.log("CLOSED!!!!!!!!!!!")

    def update_element(self, args):
        window.console.log("UPDATE!!!!!!!!!!!")
        window.console.log(args)
        id = args.get('id')
        x = args.get('x')
        y = args.get('y')
        self.elements[id].move_to_pos(x, y)

    def add_element(self, args):
        """Adds one element to the world"""
        window.console.log("add_element")
        window.console.log(args)
        id = args.get('id')
        visual_element = sound_element = None
        # if has an image
        img = args.get('img')
        if img:
            x = args.get('x')
            y = args.get('y')
            # Check if is this player avatar
            if id == "avatar_" + self.name:
                visual_element = window.game.add.sprite(x, y, img)
                # Fix 0 beeing converted to null by Brython
                arcade = window.Phaser.Physics.ARCADE
                if not arcade:
                    arcade = 0
                window.game.physics.enable(visual_element, arcade)
                window.game.camera.follow(visual_element)
                window.avatar = visual_element
                window.setInterval(self.slow_update, 100)
            else:
                visual_element = window.group.create(x, y, img)
                visual_element.body.immovable = True
            # if has an animation
            animation = args.get('animation')
            if animation:
                visual_element.animations.add(animation)
                animation_speed = args.get('animation_speed', 10)
                visual_element.animations.play(
                    animation, animation_speed, True)

            set_filter(visual_element)

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

        element = Element(visual_element, sound_element)
        self.elements[id] = element

        window.console.log("add_element-fim")
