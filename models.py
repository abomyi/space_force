import random

import pygame

from settings import img_player, img_bullet, img_rocks, shoot_sound, all_sprites, rock_sprites, bullet_sprites, \
    explore_animation, img_buffs, buff_sprites


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

        # 設定血量
        self.health_default = 100
        self.health = self.health_default

        # 設定生命
        self.lives = 3
        self.hidden = False
        self.hide_time = 0

        # 設定武器BUFF
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if self.hidden and now - self.hide_time > 1000 and self.lives > 0:
            self.hidden = False
            self.rect.center = (self.screen_weight / 2, self.screen_height - 20)

        if self.hidden:
            # 如果物件處於消失狀態，禁止任何操作
            return

        if self.gun > 1 and now - self.gun_time > 3000:
            self.gun -= 1
            self.gun_time = now

        # 根據玩家按下的方向鍵，控制物件位移
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed_x
        elif key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        if key_pressed[pygame.K_UP]:
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

    def shoot(self):
        if self.hidden:
            # 隱形狀態不能射擊
            return

        if self.gun == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullet_sprites.add(bullet)
            shoot_sound.play()
        else:
            bullet1 = Bullet(self.rect.left, self.rect.top)
            bullet2 = Bullet(self.rect.right, self.rect.top)
            all_sprites.add(bullet1, bullet2)
            bullet_sprites.add(bullet1, bullet2)
            shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (-self.screen_weight, -self.screen_height)

    def die(self):
        self.hide()
        self.health = self.health_default
        self.lives -= 1

    def heal(self):
        """
        吃到治療寶物時恢復生命
        """
        self.health += 20
        if self.health >= self.health_default:
            self.health = self.health_default

    def gun_up(self):
        if self.gun == 1:
            self.gun += 1
        self.gun_time = pygame.time.get_ticks()


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

        self.rect.x = random.randint(0, self.screen_weight - self.rect.width)
        self.rect.y = random.randint(-150, -100)
        self.speed_x = random.randint(-3, 3)  # 往左或往右偏移
        self.speed_y = random.randint(2, 10)
        self.rotate_degree = self.speed_x

        self.rotate_degree_total = 0

    @classmethod
    def create_rocks(cls, groups=None, num=1):
        if not groups:
            groups = [all_sprites, rock_sprites]

        for i in range(num):
            new_rock = cls()
            for group in groups:
                group.add(new_rock)

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top > self.screen_height or self.rect.left > self.screen_weight or self.rect.right < 0:
            # 當石頭超出邊界時，直接刪除這個石頭並建立新的石頭(從上面掉下來)
            self.kill()
            Rock.create_rocks()

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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explore_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update_time = pygame.time.get_ticks()  # 紀錄建立物件後經過了幾毫秒
        self.frame_rate = 30  # 每幾毫秒更新一次

    @classmethod
    def create_animate(cls, center, size):
        animate = cls(center, size)
        all_sprites.add(animate)
        return animate

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.frame_rate:
            self.last_update_time = now
            self.frame += 1
            if self.frame == len(explore_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explore_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Buff(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)

        self.screen_weight, self.screen_height = pygame.display.get_surface().get_size()
        self.category = random.choice(['heal', 'gun'])
        self.image = img_buffs[self.category]
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = 3

    @classmethod
    def create_buff(cls, center, groups=None):
        if not groups:
            groups = [all_sprites, buff_sprites]

        buff = cls(center)
        for group in groups:
            group.add(buff)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > self.screen_height:
            self.kill()
