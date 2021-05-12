from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Layout, Divider, Label, Button, Frame
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, StopApplication, NextScene
import sys


class MainWindowFrame(Frame):
    def __init__(self, screen):
        Frame.__init__(self, screen, screen.height * 2 // 3, screen.width * 2 // 3, has_border=True, name="Main Window")

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Divider())
        layout.add_widget(Label("Scribepy", align='^'))

        options_layout = Layout([1, 1, 1, 1, 1])
        self.add_layout(options_layout)
        options_layout.add_widget(Button("Browser", self._show_browser), 0)
        options_layout.add_widget(Button("Quit", self._quit), 4)

        self.fix()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord("q"), ord("Q")]:
                self._quit()

        return Frame.process_event(self, event)

    def _show_browser(self):
        raise NextScene("Scribepy File Browser")

    def _quit(self):
        raise StopApplication("Quit Application")
