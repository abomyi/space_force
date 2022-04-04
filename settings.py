import os

import pygame

# 初始化pygame & 音效
pygame.init()
pygame.mixer.init()

# 設定視窗大小
screen = pygame.display.set_mode((500, 600))

# 設定視窗標題
pygame.display.set_caption('視窗標題')

# 載入圖片
img_bg = pygame.image.load(os.path.join('img', 'background.png')).convert()
img_player = pygame.image.load(os.path.join('img', 'player.png')).convert()
img_player_life = pygame.transform.scale(img_player, (25, 19))
img_player_life.set_colorkey((0, 0, 0))
img_bullet = pygame.image.load(os.path.join('img', 'bullet.png')).convert()
img_rocks = []
for i in range(7):
    img_rocks.append(pygame.image.load(os.path.join('img', f'rock{i}.png')).convert())
explore_animation = {
    'large': [],
    'small': [],
    'player': []
}
for i in range(9):
    img_explore = pygame.image.load(os.path.join('img', f'expl{i}.png')).convert()
    img_explore.set_colorkey((0, 0, 0))
    explore_animation['large'].append(pygame.transform.scale(img_explore, (75, 75)))
    explore_animation['small'].append(pygame.transform.scale(img_explore, (30, 30)))

    img_explore_player = pygame.image.load(os.path.join('img', f'player_expl{i}.png')).convert()
    img_explore_player.set_colorkey((0, 0, 0))
    explore_animation['player'].append(img_explore_player)

img_buffs = {
    'heal': pygame.image.load(os.path.join('img', 'shield.png')).convert(),
    'gun': pygame.image.load(os.path.join('img', 'gun.png')).convert()
}

# 載入音效
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
sound_explore1 = pygame.mixer.Sound(os.path.join("sound", "expl0.wav"))
sound_explore2 = pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
sound_dead = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))

# 載入背景音樂及音量設定
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.1)

# 建立物件精靈群組
all_sprites = pygame.sprite.Group()
rock_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
buff_sprites = pygame.sprite.Group()

# 變更視窗背景顏色
# screen.fill((255, 255, 255))
# screen.blit(img_bg, (0, 0))
# pygame.display.update()

FPS = 30

font_name = pygame.font.match_font('arial')


def init_pygame_screen():
    return screen
