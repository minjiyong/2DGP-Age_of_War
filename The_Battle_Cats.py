import pico2d
import os
print(os.getenv('PYSDL2_DLL_PATH'))

from pico2d import open_canvas, delay, close_canvas
import game_framework

import logo_mode as start_mode

open_canvas(1536, 600)
game_framework.run(start_mode)
close_canvas()
