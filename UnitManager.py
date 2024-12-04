import game_framework
import game_world
from pico2d import *

from Axe_Cat import Axe_Cat
from Cat import Cat
from Cow_Cat import Cow_Cat
from Knight_Cat import Knight_Cat
from Lizard_Cat import Lizard_Cat
from Macho_Cat import Macho_Cat
from Tank_Cat import Tank_Cat
from Titan_Cat import Titan_Cat


class UnitManager:
    def __init__(self):
        self.image = load_image('Resource/Units_BC/Mobile - The Battle Cats - Cat Icons.png')
        self.font = load_font('Resource/Font/Cinzel/static/Cinzel-ExtraBold.ttf', 20)
        self.moneyfont = load_font('Resource/Font/NanumSquareRoundR.ttf', 15)
        self.gold = 10000
        self.x, self.y = 0, 0
        self.display_bounding_box = True

        self.play_time = get_time()
        self.game_time = 0

        self.cat_unlock = False
        self.machocat_unlock = False
        self.tankcat_unlock = False
        self.axecat_unlock = False
        self.knightcat_unlock = False
        self.cowcat_unlock = False
        self.lizardcat_unlock = False
        self.titancat_unlock = False

        self.unit_cooldown = 0
        self.cat_cooldown = -2.0
        self.machocat_cooldown = -2.0
        self.tankcat_cooldown = -2.5
        self.axecat_cooldown = -3.0
        self.knightcat_cooldown = -3.0
        self.cowcat_cooldown = -2.5
        self.lizardcat_cooldown = -10.0
        self.titancat_cooldown = -18.0

    def handle_event(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_F12:
                if self.display_bounding_box:
                    self.display_bounding_box = False
                elif not self.display_bounding_box:
                    self.display_bounding_box = True
                    #디버깅용 아군 전부 활성화
                    self.cat_unlock = True
                    self.machocat_unlock = True
                    self.tankcat_unlock = True
                    self.axecat_unlock = True
                    self.knightcat_unlock = True
                    self.cowcat_unlock = True
                    self.lizardcat_unlock = True
                    self.titancat_unlock = True

            # 왼쪽 마우스 버튼 클릭 시
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                print(f"Mouse clicked at ({self.x}, {self.y})")  # 클릭 좌표 출력
                # 클릭된 위치가 지정된 영역에 해당하면
                if 33 < self.x < 106 and 512 < self.y < 568:
                    if self.cat_unlock:
                        self.make_Cat()
                elif 111 < self.x < 184 and 512 < self.y < 568:
                    if self.machocat_unlock:
                        self.make_Macho_Cat()
                elif 189 < self.x < 262 and 512 < self.y < 568:
                    if self.tankcat_unlock:
                        self.make_Tank_Cat()
                elif 267 < self.x < 340 and 512 < self.y < 568:
                    if self.axecat_unlock:
                        self.make_Axe_Cat()
                elif 345 < self.x < 418 and 512 < self.y < 568:
                    if self.knightcat_unlock:
                        self.make_Knight_Cat()
                elif 423 < self.x < 496 and 512 < self.y < 568:
                    if self.cowcat_unlock:
                        self.make_Cow_Cat()
                elif 501 < self.x < 574 and 512 < self.y < 568:
                    if self.lizardcat_unlock:
                        self.make_Lizard_Cat()
                elif 579 < self.x < 652 and 512 < self.y < 568:
                    if self.titancat_unlock:
                        self.make_Titan_Cat()

            elif event.type == SDL_MOUSEMOTION:
                self.x, self.y = event.x, 600 - 1 - event.y  # y좌표 보정


    def update(self):
        pass

    def draw(self):
        #gold
        x, y  = 1380, 530
        text = f'Gold: {self.gold}'
        self.font.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
        self.font.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
        self.font.draw(x, y - 1, text, (0, 0, 0))  # 아래
        self.font.draw(x, y + 1, text, (0, 0, 0))  # 위
        self.font.draw(x, y, text, (255, 223, 99))

        #play time
        x, y = 1380, 560
        self.game_time = int(get_time() - self.play_time)
        text = f'Time: {self.game_time}'
        self.font.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
        self.font.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
        self.font.draw(x, y - 1, text, (0, 0, 0))  # 아래
        self.font.draw(x, y + 1, text, (0, 0, 0))  # 위
        self.font.draw(x, y, text, (99, 99, 223))

        #cat
        if self.cat_unlock:
            self.image.clip_composite_draw(5, 1452, 146, 113, 0, '', 70, 540, 73, 56) # x + 78
            x, y = 62, 523
            text = f'100원'
            self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
            self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
            self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
            self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
            self.moneyfont.draw(x, y, text, (255, 223, 99))
            cat_least_time = 2.0 - (get_time() - self.cat_cooldown)
            if cat_least_time > 0.0:
                x, y = 70, 540
                text = f'{int(cat_least_time) + 1}'
                self.font.draw(x - 2, y, text, (255, 255, 255))  # 왼쪽
                self.font.draw(x + 2, y, text, (255, 255, 255))  # 오른쪽
                self.font.draw(x, y - 2, text, (255, 255, 255))  # 아래
                self.font.draw(x, y + 2, text, (255, 255, 255))  # 위
                self.font.draw(x, y, text, (50, 50, 50))

        #machocat
        if self.machocat_unlock:
            self.image.clip_composite_draw(155, 1452, 146, 113, 0, '', 148, 540, 73, 56)
            x, y = 140, 523
            text = f'150원'
            self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
            self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
            self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
            self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
            self.moneyfont.draw(x, y, text, (255, 223, 99))
            machocat_least_time = 2.0 - (get_time() - self.machocat_cooldown)
            if machocat_least_time > 0.0:
                x, y = 148, 540
                text = f'{int(machocat_least_time) + 1}'
                self.font.draw(x - 2, y, text, (255, 255, 255))  # 왼쪽
                self.font.draw(x + 2, y, text, (255, 255, 255))  # 오른쪽
                self.font.draw(x, y - 2, text, (255, 255, 255))  # 아래
                self.font.draw(x, y + 2, text, (255, 255, 255))  # 위
                self.font.draw(x, y, text, (50, 50, 50))

        #tankcat
        if self.tankcat_unlock:
            self.image.clip_composite_draw(464, 1452, 146, 113, 0, '', 226, 540, 73, 56)
            x, y = 218, 523
            text = f'200원'
            self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
            self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
            self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
            self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
            self.moneyfont.draw(x, y, text, (255, 223, 99))
            tankcat_least_time = 2.5 - (get_time() - self.tankcat_cooldown)
            if tankcat_least_time > 0.0:
                x, y = 226, 540
                text = f'{int(tankcat_least_time) + 1}'
                self.font.draw(x - 2, y, text, (255, 255, 255))  # 왼쪽
                self.font.draw(x + 2, y, text, (255, 255, 255))  # 오른쪽
                self.font.draw(x, y - 2, text, (255, 255, 255))  # 아래
                self.font.draw(x, y + 2, text, (255, 255, 255))  # 위
                self.font.draw(x, y, text, (50, 50, 50))

        #axecat
        if self.axecat_unlock:
            self.image.clip_composite_draw(923, 1452, 146, 113, 0, '', 304, 540, 73, 56)
            x, y = 296, 523
            text = f'300원'
            self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
            self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
            self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
            self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
            self.moneyfont.draw(x, y, text, (255, 223, 99))
            axecat_least_time = 3.0 - (get_time() - self.axecat_cooldown)
            if axecat_least_time > 0.0:
                x, y = 304, 540
                text = f'{int(axecat_least_time) + 1}'
                self.font.draw(x - 2, y, text, (255, 255, 255))  # 왼쪽
                self.font.draw(x + 2, y, text, (255, 255, 255))  # 오른쪽
                self.font.draw(x, y - 2, text, (255, 255, 255))  # 아래
                self.font.draw(x, y + 2, text, (255, 255, 255))  # 위
                self.font.draw(x, y, text, (50, 50, 50))

        #knightcat
        if self.knightcat_unlock:
            self.image.clip_composite_draw(1073, 1452, 146, 113, 0, '', 382, 540, 73, 56)
            x, y = 374, 523
            text = f'450원'
            self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
            self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
            self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
            self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
            self.moneyfont.draw(x, y, text, (255, 223, 99))
            knightcat_least_time = 3.0 - (get_time() - self.knightcat_cooldown)
            if knightcat_least_time > 0.0:
                x, y = 382, 540
                text = f'{int(knightcat_least_time) + 1}'
                self.font.draw(x - 2, y, text, (255, 255, 255))  # 왼쪽
                self.font.draw(x + 2, y, text, (255, 255, 255))  # 오른쪽
                self.font.draw(x, y - 2, text, (255, 255, 255))  # 아래
                self.font.draw(x, y + 2, text, (255, 255, 255))  # 위
                self.font.draw(x, y, text, (50, 50, 50))

        #cowcat
        if self.cowcat_unlock:
            self.image.clip_composite_draw(1841, 1452, 146, 113, 0, '', 460, 540, 73, 56)
            x, y = 452, 523
            text = f'400원'
            self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
            self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
            self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
            self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
            self.moneyfont.draw(x, y, text, (255, 223, 99))
            cowcat_least_time = 2.5 - (get_time() - self.cowcat_cooldown)
            if cowcat_least_time > 0.0:
                x, y = 460, 540
                text = f'{int(cowcat_least_time) + 1}'
                self.font.draw(x - 2, y, text, (255, 255, 255))  # 왼쪽
                self.font.draw(x + 2, y, text, (255, 255, 255))  # 오른쪽
                self.font.draw(x, y - 2, text, (255, 255, 255))  # 아래
                self.font.draw(x, y + 2, text, (255, 255, 255))  # 위
                self.font.draw(x, y, text, (50, 50, 50))

        #lizardcat
        if self.lizardcat_unlock:
            self.image.clip_composite_draw(3218, 1452, 146, 113, 0, '', 538, 540, 73, 56)
            x, y = 521, 523
            text = f'1000원'
            self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
            self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
            self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
            self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
            self.moneyfont.draw(x, y, text, (255, 223, 99))
            lizardcat_least_time = 10.0 - (get_time() - self.lizardcat_cooldown)
            if lizardcat_least_time > 0.0:
                x, y = 538, 540
                text = f'{int(lizardcat_least_time) + 1}'
                self.font.draw(x - 2, y, text, (255, 255, 255))  # 왼쪽
                self.font.draw(x + 2, y, text, (255, 255, 255))  # 오른쪽
                self.font.draw(x, y - 2, text, (255, 255, 255))  # 아래
                self.font.draw(x, y + 2, text, (255, 255, 255))  # 위
                self.font.draw(x, y, text, (50, 50, 50))

        #titancat
        if self.titancat_unlock:
            self.image.clip_composite_draw(3677, 1452, 146, 113, 0, '', 616, 540, 73, 56)
            x, y = 599, 523
            text = f'2000원'
            self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
            self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
            self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
            self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
            self.moneyfont.draw(x, y, text, (255, 223, 99))
            titancat_least_time = 18.0 - (get_time() - self.titancat_cooldown)
            if titancat_least_time > 0.0:
                x, y = 616, 540
                text = f'{int(titancat_least_time) + 1}'
                self.font.draw(x - 2, y, text, (255, 255, 255))  # 왼쪽
                self.font.draw(x + 2, y, text, (255, 255, 255))  # 오른쪽
                self.font.draw(x, y - 2, text, (255, 255, 255))  # 아래
                self.font.draw(x, y + 2, text, (255, 255, 255))  # 위
                self.font.draw(x, y, text, (50, 50, 50))


        if self.display_bounding_box:
            draw_rectangle(33, 512, 106, 568)       # x - 37, x + 36
            draw_rectangle(111, 512, 184, 568)
            draw_rectangle(189, 512, 262, 568)
            draw_rectangle(267, 512, 340, 568)
            draw_rectangle(345, 512, 418, 568)
            draw_rectangle(423, 512, 496, 568)
            draw_rectangle(501, 512, 574, 568)
            draw_rectangle(579, 512, 652, 568)

    def make_Cat(self):
        if get_time() - self.unit_cooldown> 1.0:
            if get_time() - self.cat_cooldown > 2.0:
                if self.gold >= 100:
                    unit = Cat()
                    game_world.add_object(unit)
                    game_world.add_collision_pair('BC:Enemy', unit, None)
                    self.gold -= 100
                    self.unit_cooldown = get_time()
                    self.cat_cooldown = get_time()
                    print('madecat')

    def make_Macho_Cat(self):
        if get_time() - self.unit_cooldown> 1.0:
            if get_time() - self.machocat_cooldown > 2.0:
                if self.gold >= 150:
                    unit = Macho_Cat()
                    game_world.add_object(unit)
                    game_world.add_collision_pair('BC:Enemy', unit, None)
                    self.gold -= 150
                    self.unit_cooldown = get_time()
                    self.machocat_cooldown = get_time()
                    print('mademachocat')

    def make_Tank_Cat(self):
        if get_time() - self.unit_cooldown> 1.0:
            if get_time() - self.tankcat_cooldown > 2.5:
                if self.gold >= 200:
                    unit = Tank_Cat()
                    game_world.add_object(unit)
                    game_world.add_collision_pair('BC:Enemy', unit, None)
                    self.gold -= 200
                    self.unit_cooldown = get_time()
                    self.tankcat_cooldown = get_time()
                    print('madetankcat')

    def make_Axe_Cat(self):
        if get_time() - self.unit_cooldown> 1.0:
            if get_time() - self.axecat_cooldown > 3.0:
                if self.gold >= 300:
                    unit = Axe_Cat()
                    game_world.add_object(unit)
                    game_world.add_collision_pair('BC:Enemy', unit, None)
                    self.gold -= 300
                    self.unit_cooldown = get_time()
                    self.axecat_cooldown = get_time()
                    print('madeaxecat')

    def make_Knight_Cat(self):
        if get_time() - self.unit_cooldown> 1.0:
            if get_time() - self.knightcat_cooldown > 3.0:
                if self.gold >= 450:
                    unit = Knight_Cat()
                    game_world.add_object(unit)
                    game_world.add_collision_pair('BC:Enemy', unit, None)
                    self.gold -= 450
                    self.unit_cooldown = get_time()
                    self.knightcat_cooldown = get_time()
                    print('madeknightcat')

    def make_Cow_Cat(self):
        if get_time() - self.unit_cooldown> 1.0:
            if get_time() - self.cowcat_cooldown > 2.5:
                if self.gold >= 400:
                    unit = Cow_Cat()
                    game_world.add_object(unit)
                    game_world.add_collision_pair('BC:Enemy', unit, None)
                    self.gold -= 400
                    self.unit_cooldown = get_time()
                    self.cowcat_cooldown = get_time()
                    print('madecowcat')

    def make_Lizard_Cat(self):
        if get_time() - self.unit_cooldown> 1.0:
            if get_time() - self.lizardcat_cooldown > 10.0:
                if self.gold >= 1000:
                    unit = Lizard_Cat()
                    game_world.add_object(unit)
                    game_world.add_collision_pair('BC:Enemy', unit, None)
                    self.gold -= 1000
                    self.unit_cooldown = get_time()
                    self.lizardcat_cooldown = get_time()
                    print('madelizardcat')

    def make_Titan_Cat(self):
        if get_time() - self.unit_cooldown> 1.0:
            if get_time() - self.titancat_cooldown > 18.0:
                if self.gold >= 2000:
                    unit = Titan_Cat()
                    game_world.add_object(unit)
                    game_world.add_collision_pair('BC:Enemy', unit, None)
                    self.gold -= 2000
                    self.unit_cooldown = get_time()
                    self.titancat_cooldown = get_time()
                    print('madetitancat')