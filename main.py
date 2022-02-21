import os

import pygame

# 初始化pygame
from models import Player, Rock
from settings import img_bg, init_pygame_screen, FPS, font_name, sound_explore1, sound_explore2, all_sprites, \
    rock_sprites, bullet_sprites

screen = init_pygame_screen()

clock = pygame.time.Clock()

# 建立玩家物件
player = Player()
all_sprites.add(player)

# 建立石頭物件
Rock.create_rocks(num=9)

score = 0  # 遊戲分數

# 將上述關於遊戲視窗的設定全部套用、更新
pygame.display.update()


def draw_text(surf, text, size, x, y):
    """

    :param surf:
    :param text:
    :param size:
    :param x:
    :param y:
    :return:
    """
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


# 播放背景音樂(永不停止)
pygame.mixer.music.play(-1)

running = True
while running:
    # 維持遊戲視窗
    clock.tick(FPS)  # 程式一秒鐘能執行幾次

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 執行物件精靈群組裡面每一個物件精靈的update()
    all_sprites.update()

    # 當子彈跟石頭有碰撞時，刪除這兩個物件
    hit_rocks = pygame.sprite.groupcollide(rock_sprites, bullet_sprites, True, True)
    for hit_rock in hit_rocks:
        rock_radius = hit_rock.radius
        score += rock_radius

        # 播放石頭爆炸音效(目前石頭半徑約為7~48不等，這邊設計是夠大的石頭才會播放A音效，反之B音效)
        if rock_radius > 20:
            sound_explore1.play()
        else:
            sound_explore2.play()

        Rock.create_rocks()

    # 判斷石頭是否跟碰撞主角碰撞 (預設是矩形碰撞模式，這裡改成用圓形檢查碰撞較為準確)
    hits = pygame.sprite.spritecollide(player, rock_sprites, False, pygame.sprite.collide_circle)
    # if hits:
    #     running = False

    # 更新畫面顯示
    # screen.fill((255, 255, 255))  # 每次更新畫面的時候都要重設整個佈局(不然之前渲染的東西會一直停留在畫面上)，這裡會每次都先刷新成空白
    screen.blit(img_bg, (0, 0))
    all_sprites.draw(screen)  # 顯示所有角色物件
    draw_text(screen, f'score: {int(score)}', 18, screen.get_width() / 2, 10)
    pygame.display.update()  # 套用上述所有更動到視窗呈現

pygame.quit()
