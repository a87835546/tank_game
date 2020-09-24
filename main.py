import pygame
import random

from pygame.sprite import Sprite

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(0, 255, 255)


class BaseItem(Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        #
        # # Create an image of the block, and fill it with a color.
        # # This could also be an image loaded from the disk.
        # self.image = pygame.Surface([width, height])
        # self.image.fill(color)
        #
        # # Fetch the rectangle object that has the dimensions of the image
        # # Update the position of this object by setting the values of rect.x and rect.y
        # self.rect = self.image.get_rect()


class MainGame(object):
    window = None
    my_tank = None
    enemy_tank_list = []
    enemy_tank_count = 10
    MY_BULLET_COUNT = 3  # 我方坦克最多的子弹发射数量

    my_bullet_list = []
    enemy_bullt_list = []
    expload_list = []

    wall_list = []
    def __init__(self):
        super().__init__()

    def start_game(self):
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('坦克大战1.0')
        self.init_my_tank()
        self.init_enemy_tank()
        clock = pygame.time.Clock()
        self.create_wall()

        while True:

            MainGame.window.fill(BG_COLOR)
            self.get_event_list()
            MainGame.window.blit(self.get_text_surface('敌方剩余坦克数量%d' % len(MainGame.enemy_tank_list)), (10, 10))
            if self.my_tank is not None and self.my_tank.live:
                self.my_tank.display_tank()
            else:
                MainGame.my_tank = None
            self.show_enemy_tank()
            self.show_my_bullet()
            self.show_enemy_bullet()
            self.show_boom()

            self.show_wall()
            if self.my_tank is not None \
                    and self.my_tank.live and \
                    not MainGame.my_tank.stop:
                MainGame.my_tank.move()

            pygame.display.update()
            clock.tick(60)

    def init_my_tank(self):
        MainGame.my_tank = Tank(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


    # 初始化敌方坦克
    def init_enemy_tank(self):
        for i in range(MainGame.enemy_tank_count):
            tank = EnemyTank(self.get_random_rect()[0], self.get_random_rect()[1], 1)
            MainGame.enemy_tank_list.append(tank)

    # 随机生成坦克的坐标
    def get_random_rect(self):
        left = random.randint(0, 600)
        top = random.randint(0, 400)
        return [left, top]

    def show_enemy_tank(self):
        for tank in MainGame.enemy_tank_list:
            if tank.live:
                tank.display_tank()
                tank.random_move()
                tank.hit_wall()
                enemy_bullet = tank.shot()
                if enemy_bullet:
                    self.enemy_bullt_list.append(enemy_bullet)
            else:
                MainGame.enemy_tank_list.remove(tank)

    def show_enemy_bullet(self):
        for bullet in self.enemy_bullt_list:
            if bullet.live:
                bullet.show_bullet()
                bullet.move()
                bullet.enemy_bullet_hit_my_tank()
                bullet.bullet_hit_wall()
            else:
                self.enemy_bullt_list.remove(bullet)

    def show_my_bullet(self):
        for bullet in self.my_bullet_list:
            print('我方坦克的子弹是否存活：' + str(bullet.live))
            if bullet.live:
                bullet.show_bullet()
                bullet.move()
                bullet.my_bullet_hit_tank()
                bullet.bullet_hit_wall()
            else:
                self.my_bullet_list.remove(bullet)

    def show_boom(self):
        for expload in self.expload_list:
            if expload.live:
                expload.show_expload()
            else:
                self.expload_list.remove(expload)

    def create_wall(self):
        for i in range(1, 6):
            wall = Wall(150*i, 200)
            self.wall_list.append(wall)

    def show_wall(self):
        for wall in self.wall_list:
            wall.display_wall()

    def get_event_list(self):
        event_list = pygame.event.get()
        for event in event_list:
            # print(event.type)
            if event.type == pygame.QUIT:
                self.end_game()

            # 捕获键盘按下 上下左右的方向键
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print('点击上箭头')
                    if self.my_tank is not None \
                            and self.my_tank.live:
                        self.my_tank.direction = 'U'
                        self.my_tank.stop = False
                elif event.key == pygame.K_DOWN:
                    print('点击下箭头')
                    if self.my_tank and self.my_tank.live:
                        MainGame.my_tank.direction = 'D'
                        MainGame.my_tank.stop = False
                elif event.key == pygame.K_LEFT:
                    print('点击左箭头')
                    if self.my_tank and self.my_tank.live:
                        MainGame.my_tank.direction = 'L'
                        MainGame.my_tank.stop = False
                elif event.key == pygame.K_RIGHT:
                    print('点击右箭头')
                    if self.my_tank and self.my_tank.live:
                        MainGame.my_tank.direction = 'R'
                        MainGame.my_tank.stop = False
                elif event.key == pygame.K_SPACE:
                    print('发射子弹')
                    if len(self.my_bullet_list) < self.MY_BULLET_COUNT \
                            and self.my_tank and self.my_tank.live:
                        my_bullet = Bullet(self.my_tank)
                        if my_bullet.live:
                            print(self.my_tank.direction + str(self.my_tank.rect))
                            self.my_bullet_list.append(my_bullet)
                        else:
                            self.my_bullet_list.remove(my_bullet)
                elif event.key == pygame.K_ESCAPE:
                    if self.my_tank is None:
                        self.init_my_tank()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_UP \
                        or event.key == pygame.K_LEFT \
                        or event.key == pygame.K_DOWN:
                    if self.my_tank is not None and self.my_tank.live:
                        MainGame.my_tank.stop = True
                        print('放开按键')

    def end_game(self):
        exit()

    def get_text_surface(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('songti', 18)
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface


class Tank(BaseItem):
    def __init__(self, left, top):
        # super().__init__()
        # super(Tank, self).__init__(BG_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.imgs = {
            'U': pygame.image.load('imgs/my_tank_t.png'),
            'D': pygame.image.load('imgs/my_tank_d.png'),
            'L': pygame.image.load('imgs/my_tank_l.png'),
            'R': pygame.image.load('imgs/my_tank_r.png'),
        }
        self.direction = 'U'
        self.image = self.imgs[self.direction]
        # self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 5  # 坦克移动速度
        self.stop = True
        self.live = True
        self.old_left = left
        self.old_top = top

    def move(self):
        self.old_top = self.rect.top
        self.old_left = self.rect.left
        if self.direction == 'U':
            if self.rect.top >= 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left >= 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
        self.hit_wall()
        self.my_tank_hit_enemy_tank()

    def shot(self):
        pass

    def display_tank(self):
        MainGame.window.blit(self.imgs[self.direction], self.rect)

    def hit_wall(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.rect.left = self.old_left
                self.rect.top = self.old_top

    def my_tank_hit_enemy_tank(self):
        for tank in MainGame.enemy_tank_list:
            if MainGame.my_tank is not None and MainGame.my_tank.live and pygame.sprite.collide_rect(tank, MainGame.my_tank):
                self.rect.left = self.old_left
                self.rect.top = self.old_top

class MyTank(Tank):
    def __init__(self):
        super().__init__()
        super().direction = 'D'


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        super().__init__(left, top)
        self.imgs = {
            'U': pygame.image.load('imgs/enemy_tank_t.png'),
            'D': pygame.image.load('imgs/enemy_tank_d.png'),
            'L': pygame.image.load('imgs/enemy_tank_l.png'),
            'R': pygame.image.load('imgs/enemy_tank_r.png'),
        }
        self.direction = self.get_random_direction()
        self.enemy_image = self.imgs[self.direction]
        self.rect = self.enemy_image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.step = 50

    def get_random_direction(self):
        i = random.randint(1, 4)
        if i == 1:
            return 'U'
        elif i == 2:
            return 'D'
        elif i == 3:
            return 'L'
        elif i == 4:
            return 'R'

    def random_move(self):
        if self.step < 0:
            self.step = 50
            self.direction = self.get_random_direction()
        else:
            self.step -= 1
            self.move()
        self.my_tank_hit_enemy_tank()



    def shot(self):
        i = random.randint(1, 500)
        if i < 10:
            return Bullet(self)


class Bullet(BaseItem):
    def __init__(self, tank):
        # super().__init__()
        self.speed = 5
        self.direction = tank.direction
        self.image = pygame.image.load('./imgs/bullt.png')
        # self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.live = True  # 判断子弹是否显示

        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + self.rect.height + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        print('初始化的子弹位置：' + str(self.rect))

    def show_bullet(self):
        # print('初始化的子弹位置：' + str(self.rect))
        MainGame.window.blit(self.image, self.rect)

    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False

    # 我方子弹击中敌方坦克
    def my_bullet_hit_tank(self):
        for tank in MainGame.enemy_tank_list:
            if pygame.sprite.collide_rect(tank, self):
                print('是否击中')
                expload = Expload(tank)
                MainGame.expload_list.append(expload)
                tank.live = False
                self.live = False

    # 敌方子弹击中我方坦克
    def enemy_bullet_hit_my_tank(self):
        if MainGame.my_tank is not None and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                print('我方坦克被击中')
                expload = Expload(MainGame.my_tank)
                MainGame.expload_list.append(expload)
                MainGame.my_tank.live = False
                self.live = False

    def bullet_hit_wall(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.live = False



class Expload(object):
    def __init__(self, tank):
        super(Expload, self).__init__()
        self.tank = tank
        self.live = True  # 判断是否显示爆炸效果
        self.step = 0
        self.images = [pygame.image.load('./imgs/enemy_boom1.png'),
                       pygame.image.load('./imgs/enemy_boom2.png'),
                       pygame.image.load('./imgs/enemy_boom3.png'),
                       pygame.image.load('./imgs/enemy_boom4.png'),
                       pygame.image.load('./imgs/enemy_boom5.png'),
                       pygame.image.load('./imgs/enemy_boom6.png'),
                       pygame.image.load('./imgs/enemy_boom7.png'),
                       pygame.image.load('./imgs/enemy_boom8.png')
                       ]

    def show_expload(self):
        print('刷新图片')

        if self.step < len(self.images):
            MainGame.window.blit(self.images[self.step], self.tank.rect)
            self.step += 1
        else:
            self.step == 0
            self.live = False

class Wall(object):
    def __init__(self, left, top):
        super(Wall, self).__init__()
        self.image = pygame.image.load('./imgs/icon_parplay_down_arrow@3x.png')
        self.rect = self.image.get_rect()
        self.old_left = self.rect.left
        self.old_top = self.rect.top
        self.hp = 10
        self.left = left
        self.top = top
        self.rect.left = left
        self.rect.top = top


    def display_wall(self):
        MainGame.window.blit(self.image, self.rect)


if __name__ == '__main__':
    MainGame().start_game()
