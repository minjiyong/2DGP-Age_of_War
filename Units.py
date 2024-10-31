from pygame.examples.grid import WINDOW_WIDTH

from state_machine import StateMachine, space_down, time_out, right_down, left_down, right_up, left_up, start_event, \
    a_down
from pico2d import load_image, get_time


class Idle:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.action = 2
            boy.face_dir = -1
        elif time_out(e):
            if boy.face_dir == 1:
                boy.action = 3
            elif boy.face_dir == -1:
                boy.action = 2
        elif left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e):
            boy.action = 3
            boy.face_dir = 1
        boy.frame = 0
        boy.dir = 0
        # 시작 시간을 기록
        boy.start_time = get_time()
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
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
        cat.image.clip_draw(cat.frame * 100, cat.action * 100, 100, 100, cat.x, cat.y + 25, 100, 100)
        pass

class Cat:
    image = None
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/Units_BC/Mobile - The Battle Cats - Cat.png')
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.enemy = False
        self.state_machine = StateMachine(self)      # 소년 객체를 위한 상태 머신임을 알려줌
        self.state_machine.start(AutoRun)
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


