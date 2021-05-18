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
                #Create custom labels
                labels=True,
                axes=BarChart.X_AXIS),
            x=(screen.width - 60) // 2,
            y=(screen.height - 7) // 2,
            transparent=False, speed=2),

    def _update(self, frame_no):
        if (self.connector.player.position / self.connector.player.length) == 1:
            raise NextScene("Scribepy File Browser")
        else:
            Print._update(self, frame_no)

    def process_event(self, event):

        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord("q"), ord("Q")]:
                self.connector.player.stop()
                raise NextScene("Scribepy File Browser")
            elif event.key_code in [ord("s")]:
                self.connector.player.stop()
                raise NextScene("Scribepy File Browser")
            elif event.key_code in [ord(" ")]:
                self.connector.player.pause_play_toggle
            elif event.key_code in [ord("l"), Screen.KEY_RIGHT]:
                self.connector.player.move_to_position_seconds(self.connector.player.position + 3)
            elif event.key_code in [ord("l"), Screen.KEY_LEFT]:
                self.connector.player.move_to_position_seconds(self.connector.player.position - 3)

    def get_progress(self):
        return (self.connector.player.position / self.connector.player.length) * 100

    def set_connector(self, c):
        self.connector = c
