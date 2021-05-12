from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.renderers import BarChart
from asciimatics.effects import Print
from asciimatics.exceptions import NextScene


class ProgressBar(Print):
    def __init__(self, screen):
        Print.__init__(self, screen,
            BarChart(
                7, 60, [self.get_progress],
                char=">",
                scale=100.0,
                labels=True,
                axes=BarChart.X_AXIS),
            x=(screen.width - 60) // 2,
            y=(screen.height - 7) // 2,
            transparent=True, speed=2),


    def _update(self, frame_no):
        if (self.player.position / self.player.length) == 1:
            raise NextScene("Main Window")
        else:
            Print._update(self, frame_no)

    def process_event(self, event):

        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord("q"), ord("Q")]:
                self.player.stop()
                raise NextScene("Main Window")
            if event.key_code in [ord("s")]:
                self.player.stop()
                raise NextScene("Main Window")
            elif event.key_code in [ord(" ")]:
                self.player.pause_play_toggle
            elif event.key_code in [ord("l"), Screen.KEY_RIGHT]:
                self.player.move_to_position_seconds(self.player.position + 3)
            elif event.key_code in [ord("l"), Screen.KEY_LEFT]:
                self.player.move_to_position_seconds(self.player.position - 3)

    def setPlayer(self, p):
        self.player = p

    def get_progress(self):
        return (self.player.position / self.player.length) * 100
