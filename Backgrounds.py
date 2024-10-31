from pico2d import *

class Background:
    image = None
    # 생성자를 이용해서 객체의 초기 상태를 정의 상태를 정의함
    def __init__(self):
        if self.image == None:
            self.image = load_image('Resource/backgrounds/Hills Free (update 3.0).png')
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, 512, 256, 768, 256, 1536, 512)
    pass

