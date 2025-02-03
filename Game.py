import os
import pygame
import sys
import random
import sqlite3

pygame.init()
size = width, height = 1440, 820
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
FPS = pygame.time.Clock()
level_1_enemy_amount = 15
level_2_enemy_amount = 25
level_3_enemy_amount = 45


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    # стартовый экран
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
    # экран поражения
    text = ["К сожалению, ",
            'вы проиграли',
            "Инопланетяне захватили",
            'Землю']
    fon = pygame.transform.scale(load_image('game_over.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 250
    pygame.mixer.music.stop()
    file = 'data\\loose.mp3'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    pygame.event.wait()
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
    # экран победы и сохранение количества выстрелов в дб
    con = sqlite3.connect("high_score.sql")
    cur = con.cursor()
    cur.execute("""UPDATE score SET shots=?""", (shots,))
    con.commit()
    con.close()
    text = ["Вы отбили атаку инопланетян!",
            "Земля спасена!",
            f"Количество ваших выстрелов: {shots}"]
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


def get_high_score():
    # получения рекорда выстрелов из дб
    con = sqlite3.connect("high_score.sql")
    cur = con.cursor()
    result = cur.execute("""SELECT shots FROM score""").fetchall()
    con.close()
    return min(result)[0]


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
        # передвижение врагов
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
        # передвижение корабля и телепорт корабля на противоположную сторону, если корабль уходит за границу
        self.rect = self.rect.move(x, y)
        if self.rect.x >= width:
            self.rect.x = 0
        elif self.rect.x <= -90:
            self.rect.x = width
        if self.rect.y <= 0:
            self.rect.y = height
        elif self.rect.y >= height - 90:
            self.rect = self.rect.move(0, -y)

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
        # передвижение пули
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
        # передвижение ракеты
        self.rect = self.rect.move(0, -18)


# 4 класса с улучшениями, передвижение вниз после появления
class PowerUp(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("Power-Up.png"), (90, 90))

    # скорость корабля
    def __init__(self, pos):
        super().__init__(powerups_sprites)
        self.image = PowerUp.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.image, (pos[0], pos[1]))

    def update(self):
        self.rect = self.rect.move(0, 5)


class PowerUp2(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("Power-Up2.png"), (90, 90))

    # количество лазеров при выстреле
    def __init__(self, pos):
        super().__init__(powerups2_sprites)
        self.image = PowerUp2.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.image, (pos[0], pos[1]))

    def update(self):
        self.rect = self.rect.move(0, 5)


class PowerUp3(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("power-up3.png"), (90, 90))

    # количество мин
    def __init__(self, pos):
        super().__init__(powerups3_sprites)
        self.image = PowerUp3.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.image, (pos[0], pos[1]))

    def update(self):
        self.rect = self.rect.move(0, 5)


class PowerUp4(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("Power-Up4.png"), (90, 90))

    # перезарядка ракет
    def __init__(self, pos):
        super().__init__(powerups4_sprites)
        self.image = PowerUp4.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.image, (pos[0], pos[1]))

    def update(self):
        self.rect = self.rect.move(0, 5)


# мина при коллизии с врагом пропадает и создаёт взрыв
class Mine(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("mine.png"), (100, 100))

    def __init__(self, pos):
        super().__init__(mines_sprites)
        self.image = Mine.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.image, (pos[0], pos[1]))
        self.pos = (self.rect.x, self.rect.y)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y):
        super().__init__(explosion_sprites)
        self.frames = []
        self.cut_sheet(pygame.transform.scale(load_image("explosion.png"), (800, 400)), columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, (x, y))
        self.pos = (self.rect.x, self.rect.y)

    def cut_sheet(self, sheet, columns, rows):
        # нарезка для анимации
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


bg_image = pygame.transform.scale(load_image("space.png"), (width, height))
speed = 1.0
lasers = 1
mines = 0
time_r = 100
shots = 0
file = 'data\\music.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
pygame.event.wait()
# 3 разных уровня
for level in [level_1_enemy_amount, level_2_enemy_amount, level_3_enemy_amount]:
    kills = 0
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    projectile_sprites = pygame.sprite.Group()
    powerups_sprites = pygame.sprite.Group()
    powerups2_sprites = pygame.sprite.Group()
    powerups3_sprites = pygame.sprite.Group()
    powerups4_sprites = pygame.sprite.Group()
    explosion_sprites = pygame.sprite.Group()
    mines_sprites = pygame.sprite.Group()
    enemy_amount = level * 5
    # создание врагов
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
        # если все враги мертвы, переход на следующий уровень
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # выстрел лазерами
                shots += 1
                if lasers == 1:
                    Bullet(ship.pos)
                elif lasers == 2:
                    n = list(ship.pos)
                    n[0] -= 20
                    Bullet(tuple(n))
                    n = list(ship.pos)
                    n[0] += 20
                    Bullet(tuple(n))
                else:
                    Bullet(ship.pos)
                    n = list(ship.pos)
                    n[0] -= 20
                    Bullet(tuple(n))
                    n = list(ship.pos)
                    n[0] += 20
                    Bullet(tuple(n))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and mines > 0:
                # постановка мин
                Mine(ship.pos)
                mine_presence = True
                mines -= 1
            if event.type == pygame.KEYDOWN:
                moving = True
                if event.key == pygame.K_h:
                    # дебаг кнопка для прохождения уровня
                    enemy_amount = 0
                    print('reset')
                # передвижение корабля
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
            ship.move(x * speed, y * speed)
        # уничтожение лазера при выходе за экран
        for bullet in projectile_sprites:
            if bullet.rect.y <= 0:
                bullet.kill()
        # коллизия лазеров и врагов
        for projectile in projectile_sprites:
            for enemy1 in enemy_sprites:
                if pygame.sprite.collide_mask(enemy1, projectile):
                    n = random.randint(1, 100)
                    if n % 4 == 0 and n > 90:
                        PowerUp(projectile.rect)
                    elif n % 4 == 1 and n > 90:
                        PowerUp2(projectile.rect)
                    elif n % 4 == 2 and n > 90:
                        PowerUp3(projectile.rect)
                    elif n % 4 == 3 and n > 90:
                        PowerUp4(projectile.rect)
                    enemy1.kill()
                    projectile.kill()
                    enemy_amount -= 1
        # коллизия мин и создание взрыва
        for mine1 in mines_sprites:
            for enemy1 in enemy_sprites:
                if pygame.sprite.collide_mask(enemy1, mine1):
                    Explosion(4, 2, mine1.pos[0], mine1.pos[1])
                    mine1.kill()
                    enemy1.kill()
                    enemy_amount -= 1
        # коллизя взрыва и врагов
        for exp in explosion_sprites:
            for enemy1 in enemy_sprites:
                if pygame.sprite.collide_mask(enemy1, exp):
                    enemy1.kill()
                    print(kills)
                    kills += 1
                    if kills >= 3:
                        kills = 0
                        exp.kill()
                    enemy_amount -= 1
        # коллизия улучшений и корабля
        for powerup1 in powerups_sprites:
            if powerup1.rect.y > height:
                powerup1.kill()
        for powerup1 in powerups_sprites:
            for player in player_sprites:
                if pygame.sprite.collide_mask(powerup1, player):
                    speed += 0.125
                    powerup1.kill()
        for powerup2 in powerups2_sprites:
            for player in player_sprites:
                if pygame.sprite.collide_mask(powerup2, player):
                    lasers += 1
                    powerup2.kill()
        for powerup3 in powerups3_sprites:
            for player in player_sprites:
                if pygame.sprite.collide_mask(powerup3, player):
                    mines += 1
                    powerup3.kill()
        for powerup4 in powerups4_sprites:
            for player in player_sprites:
                if pygame.sprite.collide_mask(powerup4, player):
                    time_r -= 5
                    powerup4.kill()
        # коллизия корабля и врагов
        for enemy1 in enemy_sprites:
            for player in player_sprites:
                if pygame.sprite.collide_mask(enemy1, player):
                    # print('collision')
                    player.kill()
                    enemy1.kill()
                    alive = False
        # прорисовка всего
        screen.fill((255, 255, 255))
        screen.blit(bg_image, (0, 0))
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        projectile_sprites.draw(screen)
        player_sprites.draw(screen)
        powerups_sprites.draw(screen)
        powerups_sprites.update()
        powerups2_sprites.draw(screen)
        powerups2_sprites.update()
        powerups3_sprites.draw(screen)
        powerups3_sprites.update()
        powerups4_sprites.draw(screen)
        powerups4_sprites.update()
        explosion_sprites.draw(screen)
        explosion_sprites.update()
        mines_sprites.draw(screen)
        enemy_sprites.update()
        player_sprites.update()
        projectile_sprites.update()
        font = pygame.font.Font(None, 40)
        text_coord = 0
        # текст на экране во время игры
        for line in [f'Осталось {enemy_amount} врагов', f'Рекорд по количеству выстрелов: {get_high_score()}',
                     f'Количество мин: {mines}']:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 0
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        # таймер выстрела ракет
        time_until_rocket += 1
        if time_until_rocket % time_r == 0:
            if left_rocket % 2 == 0:
                Rocket((ship.pos[0] - 35, ship.pos[1] + 45))
            else:
                Rocket((ship.pos[0] + 35, ship.pos[1] + 45))
            left_rocket += 1
        FPS.tick(60)
# музыка
pygame.mixer.music.stop()
file = 'data\\victory.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
pygame.event.wait()
win_screen()
