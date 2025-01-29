import pygame, random

import os
import sys

pygame.init()
size = width, height = 1440, 820
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
FPS = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy_ship.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = (self.rect.x, self.rect.y)
        screen.blit(self.image, (pos[0], pos[1]))


class AllyShip(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("ally_ship.png"), (90, 90))

    def __init__(self, pos):
        super().__init__(all_sprites)
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
        super().__init__(all_sprites)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.image, (pos[0], pos[1]))
        # self.minus=10

    def update(self):
        if True or not pygame.sprite.collide_mask(self, Enemy):
            self.rect = self.rect.move(0, -10)


class Rocket(pygame.sprite.Sprite):
    image = load_image("rocket.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Rocket.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.image, (pos[0], pos[1]))
        # self.minus=10

    def update(self):
        if True or not pygame.sprite.collide_mask(self, Enemy):
            self.rect = self.rect.move(0, -18)


all_sprites = pygame.sprite.Group()
enemy = Enemy((width // 2, height // 2))
ship = AllyShip((100, 100))
running = True
moving = False
key = False
x, y = 0, 0
time_until_rocket = 0
left_rocket = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Bullet(ship.pos)
        if event.type == pygame.KEYDOWN:
            moving = True
            if event.key == pygame.K_LEFT:
                x -= 5
            if event.key == pygame.K_RIGHT:
                x += 5
            if event.key == pygame.K_UP:
                y -= 5
            if event.key == pygame.K_DOWN:
                y += 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x += 5
            if event.key == pygame.K_RIGHT:
                x -= 5
            if event.key == pygame.K_UP:
                y += 5
            if event.key == pygame.K_DOWN:
                y -= 5
    if moving:
        ship.move(x, y)
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    time_until_rocket += 1
    if time_until_rocket % 100 == 0:
        if left_rocket % 2 == 0:
            Rocket((ship.pos[0] - 35, ship.pos[1] + 45))
        else:
            Rocket((ship.pos[0] + 35, ship.pos[1] + 45))
        left_rocket += 1
    FPS.tick(60)
