import game_framework
import game_world
import play_mode
from state_machine import *
from pico2d import *

# default 아군 Run speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 3.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# default 아군 Action Speed
TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3


class Attack:
    @staticmethod
    def enter(unit, e):
        if start_event(e):
            pass
        unit.frame = 0
        unit.wait_time = get_time()
        pass
    @staticmethod
    def exit(unit, e):
        pass
    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 3
        if unit.hp <= 0:
            play_mode.unitmanager.unit_dead_sound.play()
            game_world.remove_object(unit)
        if get_time() - unit.wait_time > 2.5:
            unit.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(unit):
        if int(unit.frame) == 0:
            unit.image.clip_composite_draw(0, 236, 190, 202, 0, 'h', unit.x, unit.y - 12, 190, 202)
        elif int(unit.frame) == 1:
            unit.image.clip_composite_draw(191, 236, 166, 202, 0, 'h', unit.x, unit.y - 12, 166, 202)
        elif int(unit.frame) == 2:
            unit.image.clip_composite_draw(359, 236, 164, 202, 0, 'h', unit.x, unit.y - 12, 164, 202)
            unit.image.clip_composite_draw(524, 236, 98, 202, 0, 'h', unit.x + 66, unit.y - 12, 98, 202)
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
        if unit.hp <= 0:
            play_mode.unitmanager.unit_dead_sound.play()
            game_world.remove_object(unit)
        pass
    @staticmethod
    def draw(unit):
        if int(unit.frame) == 1:
            unit.image.clip_composite_draw(int(unit.frame) * 74 + 96, 455, 74, 194, 0, 'h', unit.x - 5, unit.y - 15, 74, 194)
        elif int(unit.frame) == 0 or 2:
            unit.image.clip_composite_draw(int(unit.frame) * 74 + 96, 455, 74, 194, 0, 'h', unit.x - 6, unit.y - 16, 74, 194)
        unit.image.clip_composite_draw(2, 455, 92, 194, 0, 'h', unit.x, unit.y, 92, 194)
        pass

class Idle:
    @staticmethod
    def enter(unit, e):
        if start_event(e):
            if not unit.enemy:
                unit.dir = 1
            elif unit.enemy:
                unit.dir = -1
        unit.frame = 0
        unit.wait_time = get_time()
        pass
    @staticmethod
    def exit(unit, e):
        pass
    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 3
        if unit.hp <= 0:
            play_mode.unitmanager.unit_dead_sound.play()
            game_world.remove_object(unit)
        if get_time() - unit.wait_time > 0.5:
            unit.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(unit):
        if int(unit.frame) == 1:
            unit.image.clip_composite_draw(int(unit.frame) * 74 + 96, 455, 74, 194, 0, 'h', unit.x - 5, unit.y - 15, 74, 194)
        elif int(unit.frame) == 0 or 2:
            unit.image.clip_composite_draw(int(unit.frame) * 74 + 96, 455, 74, 194, 0, 'h', unit.x - 6, unit.y - 16, 74, 194)
        unit.image.clip_composite_draw(2, 455, 92, 194, 0, 'h', unit.x, unit.y, 92, 194)
        pass

class newIdle:
    @staticmethod
    def enter(unit, e):
        if start_event(e):
            if not unit.enemy:
                unit.dir = 1
            elif unit.enemy:
                unit.dir = -1
        unit.frame = 0
        unit.wait_time = get_time()
        pass
    @staticmethod
    def exit(unit, e):
        pass
    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 3
        pass
    @staticmethod
    def draw(unit):
        if int(unit.frame) == 1:
            unit.image.clip_composite_draw(int(unit.frame) * 74 + 96, 455, 74, 194, 0, 'h', unit.x - 5, unit.y - 15, 74, 194)
        elif int(unit.frame) == 0 or 2:
            unit.image.clip_composite_draw(int(unit.frame) * 74 + 96, 455, 74, 194, 0, 'h', unit.x - 6, unit.y - 16, 74, 194)
        unit.image.clip_composite_draw(2, 455, 92, 194, 0, 'h', unit.x, unit.y, 92, 194)
        pass

# 아군 유닛
class Titan_Cat:
    image = None
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/Units_BC/Mobile - The Battle Cats - Titan Cat.png')
        self.font = load_font('Resource/Font/Cinzel/static/Cinzel-ExtraBold.ttf', 12)
        self.x, self.y = 80, 130
        self.frame = 0
        self.dir = 1
        self.enemy = False
        self.hp = 2400
        self.attack = 216
        self.range = 35
        self.last_attack_time = 0  # 마지막 공격 시간을 저장
        self.attack_cooldown = 1.5  # 0.5초 간격으로만 공격 가능
        self.hitted = False
        self.state_machine = StateMachine(self)      # 소년 객체를 위한 상태 머신임을 알려줌
        self.state_machine.start(AutoRun)
        self.state_machine.set_transitions(
            {
                AutoRun: {collision: Attack, make_Idle: newIdle},
                Attack: {collision: Attack, time_out: Idle, make_Idle: newIdle},
                Idle: {collision: Attack, time_out: AutoRun, make_Idle: newIdle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event( ('INPUT', event) )

    def draw(self):
        self.state_machine.draw()
        # 충돌영역 그리기
        if (play_mode.unitmanager.display_bounding_box):
            draw_rectangle(*self.get_bb())
            draw_rectangle(*self.get_attack_bb())

        x, y = self.x - 22, self.y + 100
        text = f'Hp: {self.hp}'
        self.font.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
        self.font.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
        self.font.draw(x, y - 1, text, (0, 0, 0))  # 아래
        self.font.draw(x, y + 1, text, (0, 0, 0))  # 위
        self.font.draw(x, y, text, (0, 196, 255))

    def get_bb(self):
        return self.x-35, self.y-110, self.x+35, self.y+ 20

    def get_attack_bb(self):
        return self.x + 35, self.y - 110, self.x + 30 + self.range, self.y + 10

    def handle_attack_collision(self, group, other):
        if group == 'BC:Enemy':
            current_time = get_time()

            if current_time - self.last_attack_time > self.attack_cooldown and int(self.frame) == 2:
                if self.state_machine.cur_state is not Attack:
                    self.state_machine.add_event(('MEET_OTHER_TEAM', 0))
                    play_mode.unitmanager.unit_attack_sound.play()

                other.hitted = True
                self.last_attack_time = current_time

    def handle_hit_collision(self, group, other):
        if group == 'BC:Enemy':
            if self.hitted:
                self.take_damage(other.attack)
                self.hitted = False

    def nothing_collide(self):
        self.state_machine.add_event(('NOTHING_COLLIDE', 0))

    def take_damage(self, attack):
        self.hp -= attack

    def remove_itself(self):
        game_world.remove_object(self)