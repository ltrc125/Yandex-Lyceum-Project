import os
import pygame
import sys

pygame.init()
size = width, height = 1440, 820
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
FPS = pygame.time.Clock()
level_1_enemy_amount = 10
level_2_enemy_amount = 20
level_3_enemy_amount = 40


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    # print('terminate')
    pygame.quit()
    sys.exit()


def start_screen():
    print('start_screen')
    title = ['Invasion Defender']
    instructions = ["Корабль передвигается на стрелочки и WASD",
                    "Стрельба лазером происходит на клавиши мыши",
                    "Ракеты будут выстреливаться из корабля каждые несколько секунд",
                    f'Вам придётся отбиваться от {level * 5} инопланетян!',
                    'Чтобы продолжить, нажмите Enter']
    fon = pygame.transform.scale(load_image('start.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 10
    for line in title:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 450
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(None, 40)
    text_coord = 300
    for line in instructions:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        pygame.display.flip()


def game_over():
    text = ["К сожалению, ",
            'вы проиграли',
            "Инопланетяне захватили",
            'Землю']
    fon = pygame.transform.scale(load_image('game_over.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 250
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


def win_screen():
    text = ["Вы отбили атаку инопланетян!",
            "Земля спасена!"]
    fon = pygame.transform.scale(load_image('win.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    text_coord = 0
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 350
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy_ship.png")

    def __init__(self, pos):
        super().__init__(enemy_sprites)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = (self.rect.x, self.rect.y)
        screen.blit(self.image, (pos[0], pos[1]))
        self.const = 0
        self.d = 1

    def update(self):
        if self.const < width // 19:
            self.rect = self.rect.move(10 * self.d, 0)
            self.const += 1
        elif self.rect.y >= height - 100:
            global alive
            alive = False
        else:
            self.rect = self.rect.move(0, 125)
            self.const = 0
            self.d = -self.d


class AllyShip(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("ally_ship.png"), (90, 90))

    def __init__(self, pos):
        super().__init__(player_sprites)
        self.image = AllyShip.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = (self.rect.x, self.rect.y)

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def update(self):
        self.pos = (self.rect.x + 35, self.rect.y - 45)


class Bullet(pygame.sprite.Sprite):
    image = load_image("bullet.png")

    def __init__(self, pos):
        super().__init__(projectile_sprites)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.image, (pos[0], pos[1]))

    def update(self):
        self.rect = self.rect.move(0, -10)


class Rocket(pygame.sprite.Sprite):
    image = load_image("rocket.png")

    def __init__(self, pos):
        super().__init__(projectile_sprites)
        self.image = Rocket.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.image, (pos[0], pos[1]))

    def update(self):
        if not pygame.sprite.collide_mask(self, enemy):
            self.rect = self.rect.move(0, -18)


bg_image = pygame.transform.scale(load_image("space.png"), (width, height))
for level in [level_1_enemy_amount, level_2_enemy_amount, level_3_enemy_amount]:
    all_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    projectile_sprites = pygame.sprite.Group()
    enemy_amount = level * 5
    for n in range(level):
        for i in range(5):
            enemy = Enemy((150 * i, -n * 125))
    ship = AllyShip((width // 2, height // 2))
    running = True
    moving = False
    key = False
    x, y = 0, 0
    time_until_rocket = 0
    left_rocket = 1
    alive = True
    start_screen()
    while running:
        if enemy_amount == 0:
            print('attempt')
            all_sprites.clear(screen, screen)
            enemy_sprites.clear(screen, screen)
            projectile_sprites.clear(screen, screen)
            player_sprites.clear(screen, screen)
            screen.fill((255, 255, 255))
            screen.blit(bg_image, (0, 0))
            break
        if not alive:
            game_over()
        print(enemy_amount)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                Bullet(ship.pos)
            if event.type == pygame.KEYDOWN:
                moving = True
                if event.key == pygame.K_h:
                    enemy_amount = 0
                    print('reset')
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x -= 5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x += 5
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y -= 5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y += 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x += 5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x -= 5
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y += 5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y -= 5
        if moving:
            ship.move(x, y)
        for bullet in projectile_sprites:
            if bullet.rect.y < -91:
                bullet.kill()
        for projectile in projectile_sprites:
            for enemy1 in enemy_sprites:
                if pygame.sprite.collide_mask(enemy1, projectile):
                    # print('collision')
                    enemy1.kill()
                    projectile.kill()
                    enemy_amount -= 1
        for enemy1 in enemy_sprites:
            for player in player_sprites:
                if pygame.sprite.collide_mask(enemy1, player):
                    # print('collision')
                    player.kill()
                    enemy1.kill()
                    alive = False
        screen.fill((255, 255, 255))
        screen.blit(bg_image, (0, 0))
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        projectile_sprites.draw(screen)
        player_sprites.draw(screen)
        # all_sprites.update()
        enemy_sprites.update()
        player_sprites.update()
        projectile_sprites.update()
        pygame.display.flip()
        time_until_rocket += 1
        if time_until_rocket % 100 == 0:
            if left_rocket % 2 == 0:
                Rocket((ship.pos[0] - 35, ship.pos[1] + 45))
            else:
                Rocket((ship.pos[0] + 35, ship.pos[1] + 45))
            left_rocket += 1
        FPS.tick(60)
win_screen()
