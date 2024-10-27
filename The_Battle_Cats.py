from pico2d import *
import random


# Game object class here
class Background:
    image = None
    # 생성자를 이용해서 객체의 초기 상태를 정의 상태를 정의함
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/backgrounds/Hills Free (update 3.0).png')
    def update(self):
        pass
    def draw(self):
        self.image.draw(512, 256, 1024, 512)
    pass


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def update_world():
    background.update()
    pass

def render_world():
    clear_canvas()
    background.draw()
    update_canvas()

def reset_world(): # 초기화하는 함수
    global running
    global background
    global world

    running = True
    world = []
    background = Background() # Grass 클래스를 이용해서 grass 객체 생성
    world.append(background)

open_canvas(1024, 512)

# initialization code
reset_world()

# game main loop code
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)


# finalization code

close_canvas()
