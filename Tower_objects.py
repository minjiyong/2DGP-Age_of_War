from pico2d import *

class Tower:
    image = None
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/Buildings_BC/Mobile - The Battle Cats - Cat Base.png')
        self.x, self.y = 70, 120
    def update(self):
        pass
    def draw(self):
        # 3/5 사이즈로 줄여서 출력
        self.image.clip_composite_draw(0, 0, 165, 335, 0, 'h', self.x, self.y, 99, 201)
