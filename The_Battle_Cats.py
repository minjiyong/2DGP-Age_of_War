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
        self.image.clip_draw(0, 0, 512, 256, 0, 0, 1536, 512)
    pass

class Tower:
    image = None
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/Buildings_BC/Mobile - The Battle Cats - Cat Base.png')
        self.x, self.y = 60, 100
    def update(self):
        pass
    def draw(self):
        self.image.clip_composite_draw(0, 0, 165, 335, 0, 'h', self.x, self.y, 82, 167)

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
    tower.update()
    pass

def render_world():
    clear_canvas()
    background.draw()
    tower.draw()
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
    delay(0.05)


# finalization code

close_canvas()
