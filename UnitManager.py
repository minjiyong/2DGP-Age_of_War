import game_framework
import game_world
from pico2d import *

from Cat import Cat
from Macho_Cat import Macho_Cat
from Tank_Cat import Tank_Cat


class UnitManager:
    def __init__(self):
        self.image = load_image('Resource/Units_BC/Mobile - The Battle Cats - Cat Icons.png')
        self.font = load_font('Resource/Font/Cinzel/static/Cinzel-ExtraBold.ttf', 20)
        self.gold = 10000
        self.x, self.y = 0, 0

    def handle_event(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
            # 왼쪽 마우스 버튼 클릭 시
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                print(f"Mouse clicked at ({self.x}, {self.y})")  # 클릭 좌표 출력
                # 클릭된 위치가 지정된 영역에 해당하면
                if 33 < self.x < 106 and 512 < self.y < 568:
                    self.make_Cat()
                    return
                elif 111 < self.x < 184 and 512 < self.y < 568:
                    self.make_Macho_Cat()
                elif 189 < self.x < 262 and 512 < self.y < 568:
                    self.make_Tank_Cat()

            elif event.type == SDL_MOUSEMOTION:
                self.x, self.y = event.x, 600 - 1 - event.y  # y좌표 보정


    def update(self):
        pass

    def draw(self):
        x, y  = 1380, 560
        text = f'Gold: {self.gold}'
        self.font.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
        self.font.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
        self.font.draw(x, y - 1, text, (0, 0, 0))  # 아래
        self.font.draw(x, y + 1, text, (0, 0, 0))  # 위
        self.font.draw(x, y, text, (255, 223, 99))

        self.image.clip_composite_draw(5, 1452, 146, 113, 0, '', 70, 540, 73, 56) # x + 78
        self.image.clip_composite_draw(155, 1452, 146, 113, 0, '', 148, 540, 73, 56)
        self.image.clip_composite_draw(464, 1452, 146, 113, 0, '', 226, 540, 73, 56)

        draw_rectangle(33, 512, 106, 568)       # x - 37, x + 36
        draw_rectangle(111, 512, 184, 568)
        draw_rectangle(189, 512, 262, 568)

    def make_Cat(self):
        if self.gold >= 100:
            unit = Cat()
            game_world.add_object(unit)
            game_world.add_collision_pair('BC:Enemy', unit, None)
            self.gold -= 100
            print('mademachocat')

    def make_Macho_Cat(self):
        if self.gold >= 150:
            unit = Macho_Cat()
            game_world.add_object(unit)
            game_world.add_collision_pair('BC:Enemy', unit, None)
            self.gold -= 150
            print('madecat')

    def make_Tank_Cat(self):
        if self.gold >= 200:
            unit = Tank_Cat()
            game_world.add_object(unit)
            game_world.add_collision_pair('BC:Enemy', unit, None)
            self.gold -= 200
            print('madetankcat')