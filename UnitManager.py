import game_framework
import game_world
from pico2d import *

import play_mode
from Axe_Cat import Axe_Cat
from Cat import Cat
from Cow_Cat import Cow_Cat
from Knight_Cat import Knight_Cat
from Lizard_Cat import Lizard_Cat
from Macho_Cat import Macho_Cat
from Tank_Cat import Tank_Cat
from Titan_Cat import Titan_Cat

from Dog import Dog
from Hippo import Hippo
from Snake import Snake
from Croco import Croco


class UnitManager:
    def __init__(self):
        self.image = load_image('Resource/Units_BC/Mobile - The Battle Cats - Cat Icons.png')
        self.skillimage = load_image('Resource/Units_BC/3DS - Puzzle & Dragons Super Mario Bros Edition - Skill Icons.png')
        self.godimage = load_image('Resource/Units_BC/Mobile - The Battle Cats - God Cat.png')
        self.font = load_font('Resource/Font/Cinzel/static/Cinzel-ExtraBold.ttf', 20)
        self.moneyfont = load_font('Resource/Font/NanumSquareRoundR.ttf', 15)

        self.buy_unit_sound = load_wav('Resource/sounds/Snd019.ogg')
        self.buy_unit_sound.set_volume(40)
        self.unlock_unit_sound = load_wav('Resource/sounds/Snd011.ogg')
        self.unlock_unit_sound.set_volume(40)
        self.buy_skill_sound = load_wav('Resource/sounds/Snd014.ogg')
        self.buy_skill_sound.set_volume(40)
        self.god_sound =  load_wav('Resource/sounds/Snd035.ogg')
        self.god_sound.set_volume(70)
        self.unit_attack_sound = load_wav('Resource/sounds/Snd020.ogg')
        self.unit_attack_sound.set_volume(20)
        self.unit_dead_sound = load_wav('Resource/sounds/Snd023.ogg')
        self.unit_dead_sound.set_volume(20)

        self.x, self.y = 0, 0
        self.display_bounding_box = False

        self.gold = 999
        self.gold_interval = 1
        self.interval = 0.1
        self.gold_upgrade_cost = 200

        self.play_time = get_time()
        self.last_update_time = 0
        self.game_time = 0

        self.cat_unlock = True
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

        self.god_cooldown = -200.0
        self.draw_god = False
        self.god_image_time = None

        self.selected_object = None
        self.mix1 = None
        self.mix2 = None

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

                elif 33 < self.x < 106 and 452 < self.y < 508:
                    if play_mode.tower.level < 5:
                        if self.gold > self.gold_upgrade_cost:
                            self.gold -= self.gold_upgrade_cost
                            self.gold_upgrade_cost += 100
                            self.gold_interval += 1
                            play_mode.tower.tower_levelup()
                elif 111 < self.x < 184 and 452 < self.y < 508:
                    if self.gold > 500:
                        self.gold -= 500
                        play_mode.tower.recover_tower()
                elif 189 < self.x < 262 and 452 < self.y < 508:
                    if get_time() - self.god_cooldown > 200.0:
                        self.draw_god = True
                        self.god_sound.play()

                        all_objects = game_world.get_objects(1)
                        for obj in all_objects:
                            if isinstance(obj, (Dog, Hippo, Croco, Snake)):  # 적 클래스 목록
                                obj.hp -= 150
                        self.god_cooldown = get_time()
                        print('used skill - god')

                elif 189 < self.x < 262 and 392 < self.y < 448:
                    # 둘다 넣었으면 -> 조합식에 따라 새로운 거 해금
                    if self.mix1 and self.mix2:
                        #machocat = cat + cat
                        if isinstance(self.mix1, Cat) and isinstance(self.mix2, Cat):
                            self.machocat_unlock = True
                            self.unlock_unit_sound.play()
                        #tankcat = machocat + cat
                        elif (isinstance(self.mix1, Macho_Cat) and isinstance(self.mix2, Cat)) or (isinstance(self.mix1, Cat) and isinstance(self.mix2, Macho_Cat)):
                            self.tankcat_unlock = True
                            self.unlock_unit_sound.play()
                        #Axecat = machocat + machocat
                        elif isinstance(self.mix1, Macho_Cat) and isinstance(self.mix2, Macho_Cat):
                            self.axecat_unlock = True
                            self.unlock_unit_sound.play()
                        #knightcat = axecat + axecat
                        elif isinstance(self.mix1, Axe_Cat) and isinstance(self.mix2, Axe_Cat):
                            self.knightcat_unlock = True
                            self.unlock_unit_sound.play()
                        #cowcat = axecat + cat
                        elif (isinstance(self.mix1, Axe_Cat) and isinstance(self.mix2, Cat)) or (isinstance(self.mix1, Cat) and isinstance(self.mix2, Axe_Cat)):
                            self.cowcat_unlock = True
                            self.unlock_unit_sound.play()
                        #lizardcat = cowcat + cowcat
                        elif isinstance(self.mix1, Cow_Cat) and isinstance(self.mix2, Cow_Cat):
                            self.lizardcat_unlock = True
                            self.unlock_unit_sound.play()
                        #titancat = tankcat + knightcat
                        elif (isinstance(self.mix1, Tank_Cat) and isinstance(self.mix2, Knight_Cat)) or (isinstance(self.mix1, Knight_Cat) and isinstance(self.mix2, Tank_Cat)):
                            self.titancat_unlock = True
                            self.unlock_unit_sound.play()

                    # 둘 중 하나라도 없으면
                    if self.mix1:
                        self.mix1.remove_itself()
                    if self.mix2:
                        self.mix2.remove_itself()

                    self.mix1 = None
                    self.mix2 = None

                game_world.add_collision_pair('BC:Mouse', None, self)

            elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
                game_world.remove_collision_object(self)
                if self.selected_object:
                    if 33 < self.x < 106 and 392 < self.y < 448:
                        if isinstance(self.selected_object, Cat) and not self.mix1:
                            self.mix1 = Cat()
                            self.mix1.x, self.mix1.y = 70, 420
                            self.mix1.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix1)
                        elif isinstance(self.selected_object, Macho_Cat) and not self.mix1:
                            self.mix1 = Macho_Cat()
                            self.mix1.x, self.mix1.y = 70, 420
                            self.mix1.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix1)
                        elif isinstance(self.selected_object, Tank_Cat) and not self.mix1:
                            self.mix1 = Tank_Cat()
                            self.mix1.x, self.mix1.y = 70, 420
                            self.mix1.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix1)
                        elif isinstance(self.selected_object, Axe_Cat) and not self.mix1:
                            self.mix1 = Axe_Cat()
                            self.mix1.x, self.mix1.y = 70, 420
                            self.mix1.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix1)
                        elif isinstance(self.selected_object, Knight_Cat) and not self.mix1:
                            self.mix1 = Knight_Cat()
                            self.mix1.x, self.mix1.y = 70, 420
                            self.mix1.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix1)
                        elif isinstance(self.selected_object, Cow_Cat) and not self.mix1:
                            self.mix1 = Cow_Cat()
                            self.mix1.x, self.mix1.y = 70, 420
                            self.mix1.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix1)
                        elif isinstance(self.selected_object, Lizard_Cat) and not self.mix1:
                            self.mix1 = Lizard_Cat()
                            self.mix1.x, self.mix1.y = 70, 420
                            self.mix1.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix1)
                        elif isinstance(self.selected_object, Titan_Cat) and not self.mix1:
                            self.mix1 = Titan_Cat()
                            self.mix1.x, self.mix1.y = 70, 420
                            self.mix1.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix1)

                    elif 111 < self.x < 184 and 392 < self.y < 448:
                        if isinstance(self.selected_object, Cat) and not self.mix2:
                            self.mix2 = Cat()
                            self.mix2.x, self.mix2.y = 148, 420
                            self.mix2.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix2)
                        elif isinstance(self.selected_object, Macho_Cat) and not self.mix2:
                            self.mix2 = Macho_Cat()
                            self.mix2.x, self.mix2.y = 148, 420
                            self.mix2.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix2)
                        elif isinstance(self.selected_object, Tank_Cat) and not self.mix2:
                            self.mix2 = Tank_Cat()
                            self.mix2.x, self.mix2.y = 148, 420
                            self.mix2.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix2)
                        elif isinstance(self.selected_object, Axe_Cat) and not self.mix2:
                            self.mix2 = Axe_Cat()
                            self.mix2.x, self.mix2.y = 148, 420
                            self.mix2.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix2)
                        elif isinstance(self.selected_object, Knight_Cat) and not self.mix2:
                            self.mix2 = Knight_Cat()
                            self.mix2.x, self.mix2.y = 148, 420
                            self.mix2.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix2)
                        elif isinstance(self.selected_object, Cow_Cat) and not self.mix2:
                            self.mix2 = Cow_Cat()
                            self.mix2.x, self.mix2.y = 148, 420
                            self.mix2.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix2)
                        elif isinstance(self.selected_object, Lizard_Cat) and not self.mix2:
                            self.mix2 = Lizard_Cat()
                            self.mix2.x, self.mix2.y = 148, 420
                            self.mix2.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix2)
                        elif isinstance(self.selected_object, Titan_Cat) and not self.mix2:
                            self.mix2 = Titan_Cat()
                            self.mix2.x, self.mix2.y = 148, 420
                            self.mix2.state_machine.add_event(('IDLE', 0))
                            game_world.add_object(self.mix2)

                    self.selected_object.remove_itself()
                    self.selected_object = None

            elif event.type == SDL_MOUSEMOTION:
                self.x, self.y = event.x, 600 - 1 - event.y  # y좌표 보정


    def update(self):
        # 시간 증가
        current_time = get_time()
        self.game_time = int(current_time - self.play_time)

        # 시간에 따른 돈 증가
        if  current_time - self.last_update_time >= self.interval:
            self.gold += self.gold_interval
            self.last_update_time = current_time
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

        #skill - gold
        self.skillimage.clip_composite_draw(0, 168, 73, 56, 0, '', 70, 480, 73, 56)
        x, y = 62, 463
        text = f'{self.gold_upgrade_cost}원'
        self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
        self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
        self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
        self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
        self.moneyfont.draw(x, y, text, (255, 223, 99))

        # skill - recover
        self.skillimage.clip_composite_draw(0, 112, 73, 56, 0, '', 148, 480, 73, 56)
        x, y = 140, 463
        text = f'500원'
        self.moneyfont.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
        self.moneyfont.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
        self.moneyfont.draw(x, y - 1, text, (0, 0, 0))  # 아래
        self.moneyfont.draw(x, y + 1, text, (0, 0, 0))  # 위
        self.moneyfont.draw(x, y, text, (255, 223, 99))

        # skill - god
        self.skillimage.clip_composite_draw(74, 168, 73, 56, 0, '', 226, 480, 73, 56)
        god_least_time = 200.0 - (get_time() - self.god_cooldown)
        if god_least_time > 0.0:
            x, y = 210, 480
            text = f'{int(god_least_time) + 1}'
            self.font.draw(x - 2, y, text, (255, 255, 255))  # 왼쪽
            self.font.draw(x + 2, y, text, (255, 255, 255))  # 오른쪽
            self.font.draw(x, y - 2, text, (255, 255, 255))  # 아래
            self.font.draw(x, y + 2, text, (255, 255, 255))  # 위
            self.font.draw(x, y, text, (50, 50, 50))
        # 갓 스킬 시전 시
        if self.draw_god:
            if self.god_image_time == None:
                self.god_image_time = get_time()
            self.godimage.clip_composite_draw(0, 46, 278, 260, 0, 'h', 768, 300, 556, 520)
            if get_time() - self.god_image_time > 3.0:
                self.draw_god = False
                self.god_image_time = None

        # mix1
        self.skillimage.clip_composite_draw(0, 0, 73, 56, 0, '', 70, 420, 73, 56)
        # mix2
        self.skillimage.clip_composite_draw(0, 0, 73, 56, 0, '', 148, 420, 73, 56)
        # mixbutton
        self.skillimage.clip_composite_draw(0, 56, 73, 56, 0, '', 226, 420, 73, 56)


        if self.display_bounding_box:
            #unit
            draw_rectangle(33, 512, 106, 568)       # x - 37, x + 36
            draw_rectangle(111, 512, 184, 568)
            draw_rectangle(189, 512, 262, 568)
            draw_rectangle(267, 512, 340, 568)
            draw_rectangle(345, 512, 418, 568)
            draw_rectangle(423, 512, 496, 568)
            draw_rectangle(501, 512, 574, 568)
            draw_rectangle(579, 512, 652, 568)
            #skill
            draw_rectangle(33, 452, 106, 508)
            draw_rectangle(111, 452, 184, 508)
            draw_rectangle(189, 452, 262, 508)
            #mix
            draw_rectangle(33, 392, 106, 448)
            draw_rectangle(111, 392, 184, 448)
            draw_rectangle(189, 392, 262, 448)

    def make_Cat(self):
        if get_time() - self.unit_cooldown> 1.0:
            if get_time() - self.cat_cooldown > 2.0:
                if self.gold >= 100:
                    unit = Cat()
                    game_world.add_object(unit)
                    game_world.add_collision_pair('BC:Enemy', unit, None)
                    game_world.add_collision_pair('BC:Mouse', unit, None)
                    self.gold -= 100
                    self.buy_unit_sound.play()
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
                    game_world.add_collision_pair('BC:Mouse', unit, None)
                    self.gold -= 150
                    self.buy_unit_sound.play()
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
                    game_world.add_collision_pair('BC:Mouse', unit, None)
                    self.gold -= 200
                    self.buy_unit_sound.play()
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
                    game_world.add_collision_pair('BC:Mouse', unit, None)
                    self.gold -= 300
                    self.buy_unit_sound.play()
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
                    game_world.add_collision_pair('BC:Mouse', unit, None)
                    self.gold -= 450
                    self.buy_unit_sound.play()
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
                    game_world.add_collision_pair('BC:Mouse', unit, None)
                    self.gold -= 400
                    self.buy_unit_sound.play()
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
                    game_world.add_collision_pair('BC:Mouse', unit, None)
                    self.gold -= 1000
                    self.buy_unit_sound.play()
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
                    game_world.add_collision_pair('BC:Mouse', unit, None)
                    self.gold -= 2000
                    self.buy_unit_sound.play()
                    self.unit_cooldown = get_time()
                    self.titancat_cooldown = get_time()
                    print('madetitancat')


    def get_bb(self):
        return self.x-1, self.y-1, self.x+1, self.y+1

    def get_attack_bb(self):
        return self.x-1, self.y-1, self.x+1, self.y+1

    def handle_attack_collision(self, group, other):
        if group == 'BC:Mouse':
            other.x, other.y = self.x, self.y
            self.selected_object = other

    def handle_hit_collision(self, group, other):
        if group == 'BC:Mouse':
            pass
