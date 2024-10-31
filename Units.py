from pygame.examples.grid import WINDOW_WIDTH

from state_machine import StateMachine, space_down, time_out, right_down, left_down, right_up, left_up, start_event, \
    a_down
from pico2d import *


class Attack:
    @staticmethod
    def enter(cat, e):
        if start_event(e):
            pass
        cat.frame = 0
        pass
    @staticmethod
    def exit(cat, e):
        pass
    @staticmethod
    def do(cat):
        cat.frame = (cat.frame + 1) % 4
        pass
    @staticmethod
    def draw(cat):
        cat.image.clip_composite_draw(cat.frame * 47, 166, 47, 55, 0, 'h', cat.x, cat.y, 50, 50)
        pass

class AutoRun:
    @staticmethod
    def enter(cat, e):
        if start_event(e):
            if not cat.enemy:
                cat.dir = 1
            elif cat.enemy:
                cat.dir = -1
        cat.frame = 0
        pass
    @staticmethod
    def exit(cat, e):
        pass
    @staticmethod
    def do(cat):
        cat.frame = (cat.frame + 1) % 3
        cat.x += cat.dir * 2
        pass
    @staticmethod
    def draw(cat):
        cat.image.clip_composite_draw(cat.frame * 50, 242, 50, 50, 0, 'h', cat.x, cat.y, 50, 50)
        pass

class Cat:
    image = None
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/Units_BC/Mobile - The Battle Cats - Cat.png')
        self.x, self.y = 80, 45
        self.frame = 0
        self.dir = 1
        self.action = 3
        self.enemy = False
        self.state_machine = StateMachine(self)      # 소년 객체를 위한 상태 머신임을 알려줌
        self.state_machine.start(Attack)
        self.state_machine.set_transitions(
            {
                #AutoRun : {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event( ('INPUT', event) )
        pass

    def draw(self):
        self.state_machine.draw()


