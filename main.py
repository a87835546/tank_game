import pygame, time, random

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(0, 255, 255)


class MainGame:
    window = None
    my_tank = None
    enemy_tank_list = []
    enemy_tank_count = 10

    def __init__(self):
        super().__init__()

    def start_game(self):
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('坦克大战1.0')
        MainGame.my_tank = Tank(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.init_enemy_tank()
        while True:
            time.sleep(0.02)
            MainGame.window.fill(BG_COLOR)
            self.get_event_list()
            MainGame.window.blit(self.get_text_surface('敌方剩余坦克数量%d' % 4), (10, 10))
            MainGame.my_tank.display_tank()
            MainGame.show_enemy_tank(self)
            if not MainGame.my_tank.stop:
                MainGame.my_tank.move()

            pygame.display.update()

    # 初始化敌方坦克
    def init_enemy_tank(self):
        for i in range(MainGame.enemy_tank_count):
            tank = EnmeyTank(self.get_random_rect()[0], self.get_random_rect()[1], 1)
            MainGame.enemy_tank_list.append(tank)

    # 随机生成坦克的坐标
    def get_random_rect(self):
        left = random.randint(0, 600)
        top = random.randint(0, 400)
        return [left, top]

    def show_enemy_tank(self):
        for tank in MainGame.enemy_tank_list:
            tank.display_tank()

    def get_event_list(self):
        event_list = pygame.event.get()
        for event in event_list:
            print(event.type)
            if event.type == pygame.QUIT:
                self.end_game()

            # 捕获键盘按下 上下左右的方向键
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print('点击上箭头')
                    MainGame.my_tank.direction = 'U'
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_DOWN:
                    print('点击下箭头')

                    MainGame.my_tank.direction = 'D'
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_LEFT:
                    print('点击左箭头')

                    MainGame.my_tank.direction = 'L'
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_RIGHT:
                    print('点击右箭头')

                    MainGame.my_tank.direction = 'R'
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_SPACE:
                    print('发射子弹')
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_UP \
                        or event.key == pygame.K_LEFT \
                        or event.key == pygame.K_DOWN:
                    MainGame.my_tank.stop = True
                    print('放开按键')

    def end_game(self):
        exit()

    def get_text_surface(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('songti', 18)
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface


class Tank(object):
    def __init__(self, left, top):
        super().__init__()
        self.imgs = {
            'U': pygame.image.load('imgs/icon_parplay_down_arrow@3x.png'),
            'D': pygame.image.load('imgs/icon_parplay_down_arrow@3x.png'),
            'L': pygame.image.load('imgs/icon_parplay_down_arrow@3x.png'),
            'R': pygame.image.load('imgs/icon_parplay_down_arrow@3x.png'),
        }
        self.direction = 'U'
        self.image = self.imgs[self.direction]
        self.image_rect = self.image.get_rect()
        self.image_rect.left = left
        self.image_rect.top = top
        self.speed = 5  # 坦克移动速度
        self.stop = True

    def move(self):
        if self.direction == 'U':
            if self.image_rect.top >= 0:
                self.image_rect.top -= self.speed
        elif self.direction == 'D':
            if self.image_rect.top + self.image_rect.height < SCREEN_HEIGHT:
                self.image_rect.top += self.speed
        elif self.direction == 'L':
            if self.image_rect.left >= 0:
                self.image_rect.left -= self.speed
        elif self.direction == 'R':
            if self.image_rect.left + self.image_rect.width < SCREEN_WIDTH:
                self.image_rect.left += self.speed

    def shot(self):
        pass

    def display_tank(self):
        MainGame.window.blit(self.imgs[self.direction], self.image_rect)


class MyTank(Tank):
    def __init__(self):
        super().__init__()
        super().dirction = 'D'


class EnmeyTank(Tank):
    def __init__(self, left, top, speed):
        super().__init__(left, top)
        self.imgs = {
            'U': pygame.image.load('imgs/icon_parplay_down_arrow@3x.png'),
            'D': pygame.image.load('imgs/icon_parplay_down_arrow@3x.png'),
            'L': pygame.image.load('imgs/icon_parplay_down_arrow@3x.png'),
            'R': pygame.image.load('imgs/icon_parplay_down_arrow@3x.png'),
        }
        self.direction = self.get_random_direction()
        self.enemy_image = self.imgs[self.direction]
        self.image_rect = self.enemy_image.get_rect()
        self.image_rect.left = left
        self.image_rect.top = top
        self.speed = speed

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


if __name__ == '__main__':
    MainGame().start_game()
