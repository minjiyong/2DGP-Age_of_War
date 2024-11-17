import random

from pico2d import *
import game_framework

import game_world
from Backgrounds import Background
from Hippo import Hippo
from Macho_Cat import Macho_Cat
from Tower_objects import Tower
from Cat import Cat
from UnitManager import UnitManager


def handle_events():
    unitmanager.handle_event()


def init():
    global background
    background = Background()
    game_world.add_object(background, 0)

    global unitmanager
    unitmanager = UnitManager()
    game_world.add_object(unitmanager, 0)

    global tower
    tower = Tower()
    game_world.add_object(tower, 1)
    game_world.add_collision_pair('BC:Enemy', tower, None)


    global BCs
    BCs = Macho_Cat()
    #game_world.add_object(BCs, 1)

    global Enemys
    Enemys = Hippo()
    game_world.add_object(Enemys, 1)


    #game_world.add_collision_pair('BC:Enemy', BCs, None)
    game_world.add_collision_pair('BC:Enemy', None, Enemys)


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

