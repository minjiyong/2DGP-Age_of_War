import game_framework
import game_world
import play_mode
from pico2d import *

from Croco import Croco
from Dog import Dog
from Hippo import Hippo
from Snake import Snake


class EnemyManager:
    def __init__(self):
        self.enemy_queue = []  # 적 생성 큐

        self.Dog_spawn_cooldown = get_time()
        self.Dog_max_cooldown = 10.0

        self.Croco_spawn_cooldown = get_time()
        self.Croco_max_cooldown = 13.0

        self.Hippo_spawn_cooldown = get_time()
        self.Hippo_max_cooldown = 120.0

        self.Snake_spawn_cooldown = get_time()
        self.Snake_max_cooldown = 170.0

        self.cat_unlock = False
        self.machocat_unlock = False
        self.tankcat_unlock = False
        self.axecat_unlock = False
        self.knightcat_unlock = False
        self.cowcat_unlock = False
        self.lizardcat_unlock = False
        self.titancat_unlock = False

    def spawn_enemy(self, enemy_type):
        if enemy_type == "Dog":
            return Dog()
        elif enemy_type == "Hippo":
            return Hippo()
        elif enemy_type == "Croco":
            return Croco()
        elif enemy_type == "Snake":
            return Snake()
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")

    def add_to_queue(self, enemy_type):
        enemy = self.spawn_enemy(enemy_type)
        self.enemy_queue.append(enemy)

    def process_queue(self):
        if self.enemy_queue:
            enemy = self.enemy_queue.pop(0)
            game_world.add_object(enemy, 1)
            game_world.add_collision_pair('BC:Enemy', None, enemy)
            print(f"Spawned {enemy}")

    def update(self):
        if get_time() - self.Hippo_spawn_cooldown > self.Hippo_max_cooldown:
            self.add_to_queue("Hippo")
            self.Hippo_spawn_cooldown = get_time()

        if get_time() - self.Dog_spawn_cooldown > self.Dog_max_cooldown:
            self.add_to_queue("Dog")
            self.Dog_spawn_cooldown = get_time()

        if get_time() - self.Croco_spawn_cooldown > self.Croco_max_cooldown:
            self.add_to_queue("Croco")
            self.Croco_spawn_cooldown = get_time()

        if get_time() - self.Snake_spawn_cooldown > self.Snake_max_cooldown:
            self.add_to_queue("Snake")
            self.Snake_spawn_cooldown = get_time()

        if play_mode.unitmanager.game_time == 30:
            self.Dog_max_cooldown = 8.0
            self.Snake_max_cooldown = 17.0

        if play_mode.unitmanager.game_time == 60:
            self.Dog_max_cooldown = 7.0

        if play_mode.unitmanager.game_time == 100:
            self.Dog_max_cooldown = 5.0

        if play_mode.unitmanager.game_time == 200:
            self.Hippo_max_cooldown = 100.0

        if play_mode.unitmanager.game_time == 3000:
            self.Hippo_max_cooldown = 20.0

        if play_mode.unitmanager.machocat_unlock and not self.machocat_unlock:
            self.add_to_queue("Dog")
            self.machocat_unlock = True

        if play_mode.unitmanager.tankcat_unlock and not self.tankcat_unlock:
            self.add_to_queue("Croco")
            self.tankcat_unlock = True

        if play_mode.unitmanager.knightcat_unlock and not self.knightcat_unlock:
            self.add_to_queue("Snake")
            self.knightcat_unlock = True

        self.process_queue()
        pass

    def draw(self):
        pass
