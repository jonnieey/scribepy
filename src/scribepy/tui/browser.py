import sys
from pathlib import Path

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, Layout, Widget, Label, Divider, PopUpDialog
from asciimatics.exceptions import StopApplication, NextScene
from scribepy.tui.utils.widgets import CustomFileBrowser
from scribepy.player import Player

multimedia_string = r"^.*(aac|flac|m4a|wav|ogg|mp3|mp4|tta|ac3)$"

class BrowserFrame(Frame):
    def __init__(self, screen):
        Frame.__init__(self,
            screen, screen.height * 2 // 3, screen.width * 2 // 3, has_border=True, name="Scribepy File Browser")

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)

        self.browser = CustomFileBrowser(Widget.FILL_FRAME,
                                 Path.home(),
                                 name="Scribepy File Browser",
                                 on_select=self._play,
                                 file_filter=multimedia_string,)

        layout.add_widget(Label("Scribepy File Browser"))
        layout.add_widget(Divider())
        layout.add_widget(self.browser)
        layout.add_widget(Divider())

        self.fix()

    def _play(self):
        stream = self.connector.player_play(self.browser.value)
        if stream is None:
            self.connector.run()
            raise NextScene("Progress Bar")
        else:
            self._scene.add_effect(
                PopUpDialog(self._screen, f"{stream}", ["OK"],
                        has_shadow=True, on_close=self._quit_on_ok)
            )
    @staticmethod
    def _quit_on_ok(selected):
        if selected == 0:
            raise NextScene("Scribepy File Browser")

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord("q"), ord("Q")]:
                raise NextScene("Main Window")
            if event.key_code in [ord("h")]:
                # self.browser._populate_list(os.path.abspath(os.path.join(self.browser._root, "..")))
                self.browser._populate_list(Path(self.browser._root).parent.absolute())

        return Frame.process_event(self, event)

    @staticmethod
    def _quit():
        raise StopApplication("User Quit")

    def set_connector(self, c):
        self.connector = c

