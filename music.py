from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pygame import init, USEREVENT
from pygame import mixer as mx


def load(file):
    mx.music.load(file)


def play():
    mx.music.play()


def unload():
    mx.music.unload()


class Music:
    def __init__(self) -> None:
        init()
        mx.init()
        self.paused = False
        self.MUSIC_END = USEREVENT + 1
        self.timestamp = 0
        mx.music.set_endevent(self.MUSIC_END)

    def toggle_pause(self):
        self.paused = not self.paused
        if mx.music.get_busy():
            mx.music.pause()
        else:
            mx.music.unpause()

    def get_time(self):
        return mx.music.get_pos() - self.timestamp

    def set_time(self, time):
        if self.has_ended():
            play()
        self.timestamp = mx.music.get_pos() - time
        time = time / 1000
        mx.music.rewind()
        mx.music.set_pos(time)

    def has_ended(self):
        if self.paused or mx.music.get_busy():
            return False
        return True

    def quit(self):
        self.timestamp = 0
        mx.music.fadeout(500)
        mx.music.unload()
