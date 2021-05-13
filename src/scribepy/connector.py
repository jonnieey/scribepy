from pynput import keyboard


class Connector:
    def __init__(self):
        self.player = None

    def on_press(self, key):

        #F2 increase speed

        if key == keyboard.Key.f3:
            self.player.seek(-10)

        if key == keyboard.Key.f4:
            self.player.pause()

        #F5 Restore to playback speed (1.0)

        if key == keyboard.Key.f6:
            self.player.seek(10)

        if key == keyboard.Key.f7:
            self.player.seek(-2)

        if key == keyboard.Key.f8:
            self.player.play()

        if key == keyboard.Key.f9:
            if not self.player.isPaused:
                self.player.pause()
                self.player.seek(-2)
            else:
                pass
        #F11 decrease speed

    def run(self):
        listener = keyboard.Listener(on_press=self.on_press,)
        listener.start()

    def setPlayer(self, player):
        self.player = player

