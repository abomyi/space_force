import random

import pygame

from settings import img_player, img_bullet, img_rocks


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen_weight, self.screen_height = pygame.display.get_surface().get_size()
        # self.image = pygame.Surface((50, 40))  # 設定物件大小
        # self.image.fill((0, 255, 0))  # 設定物件填滿顏色
        # self.image = img_player  # 載入圖片(依據圖片大小自動填充)
        self.image = pygame.transform.scale(img_player, (50, 38))  # 載入圖片(根據指定的寬高建立物件)
        self.image.set_colorkey((0, 0, 0))  # 將指定顏色(黑色)去除變透明
        self.rect = self.image.get_rect()
        self.radius = 20  # 判斷碰撞的半徑基礎 (適用於pygame.sprite.collide_circle)
        # pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)

        self.rect.x = 400
        self.rect.y = 200
        self.rect.centerx = self.screen_weight / 2
        self.rect.bottom = self.screen_height - 20
        self.speed_x = 10
        self.speed_y = 10

    def update(self):
        # 根據玩家按下的方向鍵，控制物件位移
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed_x
        elif key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        elif key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed_y
        elif key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed_y

        # 如果這個物件的x已經超過視窗寬高時，不再做物件位移(注意x,y跟left,right / top,bottom之間的關係，須考量到物件長寬高)
        if self.rect.x > self.screen_weight:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.x = self.screen_weight
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen_weight, self.screen_height = pygame.display.get_surface().get_size()
        # self.image = pygame.Surface((30, 40))
        # self.image.fill((255, 0, 0))
        self.image_orig = random.choice(img_rocks)
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()

        self.radius = self.rect.width / 2 * 0.8
        # pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)

        # self.rect.x = random.randint(0, self.screen_weight - self.rect.width)
        # self.rect.y = random.randint(-50, 0)
        self.speed_x = 0
        self.speed_y = 0
        self.rotate_degree = 0  # 旋轉角度
        self.reset_rock_args()

        self.rotate_degree_total = 0

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top > self.screen_height or self.rect.left > self.screen_weight or self.rect.right < 0:
            self.reset_rock_args()

    def reset_rock_args(self):
        """
        重設石頭的大小、掉落位置及速度
        """
        self.image_orig = random.choice(img_rocks)
        self.image_orig.set_colorkey((0, 0, 0))
        self.rect.x = random.randint(0, self.screen_weight - self.rect.width)
        self.rect.y = random.randint(-150, -100)
        self.speed_x = random.randint(-3, 3)  # 往左或往右偏移
        self.speed_y = random.randint(2, 10)
        self.rotate_degree = self.speed_x

    def rotate(self):
        """
        讓石頭可以旋轉
        """
        self.rotate_degree_total += self.rotate_degree
        self.rotate_degree_total %= 360  # 最大不會超過360度(1圈)
        self.image = pygame.transform.rotate(self.image_orig, -self.rotate_degree_total)

        # 重設中心點
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.screen_weight, self.screen_height = pygame.display.get_surface().get_size()
        # self.image = pygame.Surface((10, 20))
        # self.image.fill((255, 255, 0))
        self.image = img_bullet
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # self.rect.x = random.randint(0, self.screen_weight - self.rect.width)
        # self.rect.y = random.randint(-50, 0)
        # self.speed_x = random.randint(-3, 3)  # 往左或往右偏移
        # self.speed_y = random.randint(2, 10)
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
