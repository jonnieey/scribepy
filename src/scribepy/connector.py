from pynput import keyboard


class Connector:
    def __init__(self):
        self.player = None

    def on_press(self, key):

        if key == keyboard.Key.f2:
            self.player.change_tempo(4)

        if key == keyboard.Key.f3:
            self.player.seek(-10)

        if key == keyboard.Key.f4:
            self.player.pause()

        if key == keyboard.Key.f5:
            self.player.restore_tempo()

        if key == keyboard.Key.f6:
            self.player.seek(10)

        if key == keyboard.Key.f7:
            self.player.seek(-2)

        if key == keyboard.Key.f8:
            self.player.play()

        if key == keyboard.Key.f9:
            if not self.player.isPaused:
                self.player.pause()
                self.player.seek(-4)
            else:
                pass

        if key == keyboard.Key.f11:
            self.player.change_tempo(-4)

    def run(self):
        listener = keyboard.Listener(on_press=self.on_press,)
        listener.start()

    def setPlayer(self, player):
        self.player = player

