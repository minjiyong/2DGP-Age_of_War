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
        unit.image.clip_composite_draw(int(unit.frame) * 112, 52, 112, 102, 0, 'h', unit.x, unit.y, 112, 102)
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
        unit.image.clip_composite_draw(int(unit.frame) * 112, 154, 112, 102, 0, 'h', unit.x, unit.y, 112, 102)
        pass



# 적군 유닛
class Hippo:
    image = None
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/Units_Enemy/Mobile - The Battle Cats - Hippoe.png')
        self.x, self.y = 450, 70
        self.frame = 0
        self.dir = 1
        self.enemy = True
        self.hp = 1000
        self.attack = 100
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
        return self.x-53, self.y-51, self.x+53, self.y+31

    def get_attack_bb(self):
        return self.x - 53 - self.range, self.y - 51, self.x - 53, self.y + 15

    def handle_collision(self, group, other):
        if group == 'BC:Enemy':
            other.take_damage(self.attack)
            self.state_machine.add_event(('MEET_OTHER_TEAM', 0))

    def take_damage(self, attack):
        self.hp -= attack