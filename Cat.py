import game_framework
import game_world
from state_machine import StateMachine, space_down, time_out, right_down, left_down, right_up, left_up, start_event, \
    a_down, collision
from pico2d import *

# default 아군 Run speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 8.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# default 아군 Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Attack:
    @staticmethod
    def enter(unit, e):
        if start_event(e):
            pass
        unit.frame = 0
        pass
    @staticmethod
    def exit(unit, e):
        pass
    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 4
        if unit.hp < 0:
            game_world.remove_object(unit)
        pass
    @staticmethod
    def draw(unit):
        unit.image.clip_composite_draw(int(unit.frame) * 47, 166, 47, 55, 0, 'h', unit.x, unit.y, 47, 55)
        pass

class AutoRun:
    @staticmethod
    def enter(unit, e):
        if start_event(e):
            if not unit.enemy:
                unit.dir = 1
            elif unit.enemy:
                unit.dir = -1
        unit.frame = 0
        pass
    @staticmethod
    def exit(unit, e):
        pass
    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 3
        unit.x += unit.dir * RUN_SPEED_PPS * game_framework.frame_time
        if unit.hp < 0:
            game_world.remove_object(unit)
        pass
    @staticmethod
    def draw(unit):
        unit.image.clip_composite_draw(int(unit.frame) * 50, 242, 50, 50, 0, 'h', unit.x, unit.y, 50, 50)
        pass


# 아군 유닛
class Cat:
    image = None
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/Units_BC/Mobile - The Battle Cats - Cat.png')
        self.x, self.y = 80, 45
        self.frame = 0
        self.dir = 1
        self.enemy = False
        self.hp = 120
        self.attack = 96
        self.range = 20
        self.state_machine = StateMachine(self)      # 소년 객체를 위한 상태 머신임을 알려줌
        self.state_machine.start(AutoRun)
        self.state_machine.set_transitions(
            {
                AutoRun : {collision: Attack},
                Attack: {time_out: AutoRun}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event( ('INPUT', event) )

    def draw(self):
        self.state_machine.draw()
        # 충돌영역 그리기
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_attack_bb())

    def get_bb(self):
        return self.x-25, self.y-20, self.x+21, self.y+20

    def get_attack_bb(self):
        return self.x + 21, self.y - 20, self.x + 21 + self.range, self.y + 10

    def handle_collision(self, group, other):
        if group == 'BC:Enemy':
            self.state_machine.add_event(('MEET_OTHER_TEAM', 0))
            if int(self.frame) == 3:
                other.take_damage(self.attack)

    def take_damage(self, attack):
        self.hp -= attack