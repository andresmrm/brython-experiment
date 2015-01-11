from browser import window
from javascript import JSConstructor

from amoamo.tools import urljoin


class SoundManager(object):

    def __init__(self, base_folder="/"):
        self.base_folder = base_folder

        # Don't ask me why...
        try:
            self.set_listener_orientation(0, 1, 0, 0, 0, 1)
        except:
            self.set_listener_orientation(0, -1, 0, 0, 0, 1)

    def set_listener_pos(self, x, y, z=0):
        window.Howler.pos(x, y, z)

    def set_listener_orientation(self, x, y, z, ux, uy, uz):
        window.Howler.orientation(x, y, z, ux, uy, uz)

    def load(
            self,
            filenames,
            sprites=None,
            loop=False,
            autoplay=False,
            x=None,
            y=None,
            z=None):
        """filenames: list
        sprites: dict"""
        # sprites: {
        #     one: [0, 450],
        #     two: [2000, 250],
        # }

        window.console.log("SoundManager-load")
        Howl = JSConstructor(window.Howl)
        filenames = [urljoin(self.base_folder, i) for i in filenames]
        sound = Howl({"src": filenames, "sprites": sprites, "loop": loop})
        if x:
            sound.pos(x, y, z)
            # Don't ask me why...
            for i in range(2):
                sound.pannerAttr(
                    {'distanceModel': 'inverse', 'refDistance': 50,
                     'rolloffFactor': 0.05, 'panningModel': 'HRTF'})
        if autoplay:
            sound.play()

        window.console.log("SoundManager-load-fim")
        return sound
