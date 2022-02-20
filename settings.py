import os

import pygame


pygame.init()

# 設定視窗大小
screen = pygame.display.set_mode((500, 600))

# 設定視窗標題
pygame.display.set_caption('視窗標題')

# 載入圖片
img_bg = pygame.image.load(os.path.join('img', 'background.png')).convert()
img_player = pygame.image.load(os.path.join('img', 'player.png')).convert()
# img_rock = pygame.image.load(os.path.join('img', 'rock.png')).convert()
img_bullet = pygame.image.load(os.path.join('img', 'bullet.png')).convert()

img_rocks = []
for i in range(7):
    img_rocks.append(pygame.image.load(os.path.join('img', f'rock{i}.png')).convert())

# 變更視窗背景顏色
# screen.fill((255, 255, 255))
# screen.blit(img_bg, (0, 0))
# pygame.display.update()

FPS = 30

font_name = pygame.font.match_font('arial')


def init_pygame_screen():
    return screen
