import random

from pico2d import *
import game_framework

import game_world
from Backgrounds import Background
from Hippo import Hippo
from Tower_objects import Tower
from Cat import Cat


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def init():
    global background
    background = Background()
    game_world.add_object(background, 0)

    global tower
    tower = Tower()
    game_world.add_object(tower, 1)

    global BC
    BC = [Cat() for _ in range(1)]
    game_world.add_objects(BC, 1)

    global Enemy
    Enemy = [Hippo() for _ in range(1)]
    game_world.add_objects(Enemy, 1)


    #game_world.add_collision_pair('boy:ball', boy, None)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()         #소년과 볼 위치가 다 업데이트 완료
    game_world.handle_collisions()



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

