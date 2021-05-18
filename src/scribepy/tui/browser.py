import sys, os
from pathlib import Path

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, Layout, FileBrowser, Widget, Label, Divider, PopUpDialog
from asciimatics.exceptions import StopApplication, NextScene
from player import Player

class BrowserFrame(Frame):
    def __init__(self, screen):
        Frame.__init__(self,
            screen, screen.height * 2 // 3, screen.width * 2 // 3, has_border=True, name="Scribepy File Browser")

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)

        self.browser = FileBrowser(Widget.FILL_FRAME,
                                 Path.home(),
                                 name="Scribepy File Browser",
                                 on_select=self._play,)

        layout.add_widget(Label("Scribepy File Browser"))
        layout.add_widget(Divider())
        layout.add_widget(self.browser)
        layout.add_widget(Divider())

        self.fix()

    def _play(self):
        stream = self.connector.playerPlay()
        if stream is None:
            raise NextScene("Progress Bar")
        else:
            self._scene.add_effect(
                PopUpDialog(self._screen, f"{stream}", ["OK"], has_shadow=True, on_close=self._quit_on_ok)
            )
    @staticmethod
    def _quit_on_ok(selected):
        if selected == 0:
            raise NextScene("Scribepy File Browser")

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord("q"), ord("Q")]:
                raise NextScene("Main Window")

        return Frame.process_event(self, event)

    @staticmethod
    def _quit():
        raise StopApplication("User Quit")

    def setPlayer(self, p):
        self.player = p

    def setConnector(self, c):
        self.connector = c

