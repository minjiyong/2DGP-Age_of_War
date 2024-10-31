from pico2d import *
from Backgrounds import Background
from Tower_objects import Tower
import random


# Game object class here
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def update_world():
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

def reset_world(): # 초기화하는 함수
    global running
    global background
    global tower
    global world

    running = True
    world = []

    background = Background() # Grass 클래스를 이용해서 grass 객체 생성
    world.append(background)

    tower = Tower()
    world.append(tower)


open_canvas(1536, 512)

# initialization code
reset_world()

# game main loop code
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)


# finalization code

close_canvas()
