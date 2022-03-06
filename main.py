import os

import pygame

# 初始化pygame
from models import Player, Rock, Explosion
from settings import img_bg, init_pygame_screen, FPS, font_name, sound_explore1, sound_explore2, all_sprites, \
    rock_sprites, bullet_sprites, sound_dead

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
    顯示遊戲分數
    :param surf: 要畫在哪個地方
    :param text: 要顯示的文字
    :param size: 文字大小
    :param x: 要顯示在的X座標
    :param y: 要顯示在的Y座標
    """
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_health(surf, hp_default, hp, x, y):
    """
    顯示血量
    :param surf:
    :param hp_default: 原先血量 (用於計算%數)
    :param hp: 現有血量
    :param x:
    :param y:
    """
    if hp < 0:
        hp = 0
    bar_length = 100  # 血條最大長度
    bar_height = 10  # 血條高度

    # 計算血量%數
    health_percentage = (hp / hp_default) * bar_length
    # 如果血量剩餘%數大於血條長度，鎖死長度
    # health_percentage = bar_length if health_percentage > bar_length else health_percentage

    fill_rect = pygame.Rect(x, y, health_percentage, bar_height)  # 要填滿的血條
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)  # 血條外框
    pygame.draw.rect(surf, (0, 255, 0), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)


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

        # 播放爆炸動畫
        Explosion.create_animate(hit_rock.rect.center, 'large')

        Rock.create_rocks()

    # 判斷石頭是否跟碰撞主角碰撞 (預設是矩形碰撞模式，這裡改成用圓形檢查碰撞較為準確)
    hits = pygame.sprite.spritecollide(player, rock_sprites, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius
        Explosion.create_animate(hit.rect.center, 'small')

        Rock.create_rocks()
        if player.health <= 0:
            sound_dead.play()
            Explosion.create_animate(player.rect.center, 'player')
            running = False
        else:
            sound_explore1.play()

    # 更新畫面顯示
    # screen.fill((255, 255, 255))  # 每次更新畫面的時候都要重設整個佈局(不然之前渲染的東西會一直停留在畫面上)，這裡會每次都先刷新成空白
    screen.blit(img_bg, (0, 0))
    all_sprites.draw(screen)  # 顯示所有角色物件
    draw_text(screen, f'score: {int(score)}', 18, screen.get_width() / 2, 10)
    draw_health(screen, player.health_default, player.health, 5, 10)
    pygame.display.update()  # 套用上述所有更動到視窗呈現

pygame.quit()
