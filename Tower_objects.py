from pico2d import *

import game_world
import play_mode


class Tower:
    image = None
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/Buildings_BC/Mobile - The Battle Cats - Cat Base.png')
        self.font = load_font('Resource/Font/Cinzel/static/Cinzel-ExtraBold.ttf', 12)
        self.x, self.y = 70, 120
        self.level = 1
        self.hp = 800
        self.attack = 0
        self.hitted = False

    def update(self):
        if self.hp <= 0:
            game_world.remove_object(self)

    def draw(self):
        # 3/5 사이즈로 줄여서 출력
        self.image.clip_composite_draw(0, 0, 165, 335, 0, 'h', self.x, self.y, 99, 201)

        # 충돌영역 그리기
        if (play_mode.unitmanager.display_bounding_box):
            draw_rectangle(*self.get_bb())

        x, y = self.x - 25, self.y + 110
        text = f'Hp: {self.hp}'
        self.font.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
        self.font.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
        self.font.draw(x, y - 1, text, (0, 0, 0))  # 아래
        self.font.draw(x, y + 1, text, (0, 0, 0))  # 위
        self.font.draw(x, y, text, (0, 196, 255))

        x, y = self.x - 25, self.y + 130
        text = f'Level: {self.level}'
        if self.level == 5:
            text = f'Level: MAX!!'
        self.font.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
        self.font.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
        self.font.draw(x, y - 1, text, (0, 0, 0))  # 아래
        self.font.draw(x, y + 1, text, (0, 0, 0))  # 위
        self.font.draw(x, y, text, (255, 223, 99))

    def get_bb(self):
        return self.x-30, self.y-100, self.x+30, self.y+20
    def get_attack_bb(self):
        return self.x-30, self.y-100, self.x+30, self.y+20

    def handle_attack_collision(self, group, other):
        pass

    def handle_hit_collision(self, group, other):
        if group == 'BC:Enemy':
            if self.hitted:
                self.take_damage(other.attack)
                self.hitted = False
    def nothing_collide(self):
        pass

    def take_damage(self, attack):
        self.hp -= attack

    def recover_tower(self):
        self.hp += 200

    def tower_levelup(self):
        if self.level < 5:
            self.level += 1