from pico2d import *

import game_world
import game_framework
from Backgrounds import Background
from EnemyManager import EnemyManager
from Tower_objects import Tower, EnemyTower
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

    global enemymanager
    enemymanager = EnemyManager()
    game_world.add_object(enemymanager, 0)

    global tower
    tower = Tower()
    game_world.add_object(tower, 0)
    game_world.add_collision_pair('BC:Enemy', tower, None)

    global etower
    etower = EnemyTower()
    game_world.add_object(etower, 0)
    game_world.add_collision_pair('BC:Enemy', None, etower)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

