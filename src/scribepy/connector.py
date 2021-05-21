from pynput import keyboard

class Connector:
    """
    A class to interact with the pynput module.
    """

    def __init__(self):
        self.player = None

    def on_press(self, key):
        """
        Map keybindings to player functions.

        Returns:
            None.
        """

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
        """
        Start pynput keyboard listener.

        Returns:
            None.
        """
        listener = keyboard.Listener(on_press=self.on_press,)
        listener.start()

    def set_player(self, player):
        """
        Set connector attribute player.

        Arguments:
            player: Player instance.

        Returns:
            None.
        """
        self.player = player

    def set_browser(self, browser):
        """
        Set connector attribute browser.

        Arguments:
            browser: Browser instance

        Returns:
            None.
        """
        self.browser = browser

    def player_play(self, file):
        """
        Play connector channel stream.

        Arguments:
            file: File to play.
        Returns:
            None if successfull, Error message if fails.
        """
        stream = self.player.create_file_stream(file)
        if stream is None:
            self.run()
            self.player.play()
            return None
        else:
            return stream['error']

    def increase_volume(self):
        """
        Increase output master volume

        Return:
            None
        """
        curr_volume = self.player.volume
        self.player.set_volume(curr_volume + 0.05)

    def decrease_volume(self):
        """
        Decrease output master volume

        Return:
            None
        """
        curr_volume = self.player.volume
        self.player.set_volume(curr_volume - 0.05)
