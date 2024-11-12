from pico2d import open_canvas, delay, close_canvas
import game_framework

import play_mode as start_mode

open_canvas(1536, 512)
game_framework.run(start_mode)
close_canvas()
