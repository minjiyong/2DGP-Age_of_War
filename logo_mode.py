from pico2d import *

import game_framework
import play_mode


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
            game_framework.change_mode(play_mode)


def init():
    global background
    global font
    global running
    global bgm

    background = load_image('Resource/backgrounds/469414648_1073225591261641_3221111802490518487_n.png')
    font = load_font('Resource/Font/NanumSquareRoundR.ttf', 50)
    bgm = load_music('Resource/sounds/Snd003.ogg')
    running = True

    bgm.set_volume(40)
    bgm.repeat_play()


def finish():
    global background
    global font
    global bgm

    del background
    del font
    del bgm
    pass


def update():
    pass


def draw():
    clear_canvas()
    background.clip_draw(0, 0, 960, 356, 768, 300, 1536, 600)

    x, y = 450, 150
    text = f'PRESS ANY KEY TO START...'

    font.draw(x - 1, y, text, (0, 0, 0))  # 왼쪽
    font.draw(x + 1, y, text, (0, 0, 0))  # 오른쪽
    font.draw(x, y - 1, text, (0, 0, 0))  # 아래
    font.draw(x, y + 1, text, (0, 0, 0))  # 위
    font.draw(x, y, text, (255, 112, 0))
    update_canvas()

def pause():
    pass

def resume():
    pass

