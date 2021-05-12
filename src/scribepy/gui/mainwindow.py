from asciimatics.widgets import Layout, Divider, Label, Button, Frame
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, StopApplication
import sys


class MainWindow(Frame):
    def __init__(self, screen):
        Frame.__init__(self, screen, screen.height * 2 // 3, screen.width * 2 // 3, has_border=True, name="Main Window")

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Divider())
        layout.add_widget(Label("Scribepy", align='^'))

        options_layout = Layout([1, 1, 1, 1, 1])
        self.add_layout(options_layout)
        options_layout.add_widget(Button("Browser", self._show_browser), 0)
        options_layout.add_widget(Button("Prev", self._previous), 1)
        options_layout.add_widget(Button("Play/Pause", self._play), 2)
        options_layout.add_widget(Button("Next", self._next), 3)
        options_layout.add_widget(Button("Quit", self._quit), 4)

        self.fix()

    def _show_browser(self):
        pass
    def _previous(self):
        pass
    def _play(self):
        pass
    def _next(self):
        pass
    def _quit(self):
        raise StopApplication("Quit Application")

def demo(screen, old_scene):
    scenes = []
    scenes.append(Scene([MainWindow(screen)], -1, name="Main Window"))
    screen.play(scenes, start_scene = old_scene)

if __name__ == "__main__":
    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


