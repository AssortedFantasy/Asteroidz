import pygame as pg
from pathlib import Path
import random

WIDTH, HEIGHT = 1280, 720


class Game:
    def __init__(self):
        self.asteroid_sprites = pg.sprite.Group()
        self.missile_sprites = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()

    def add_random_asteroid(self):
        size = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                              [1, 2, 4, 8, 8, 8, 5, 3, 2, 1, 1])[0]

        posx = random.randrange(0, WIDTH)
        posy = random.randrange(0, HEIGHT)

        vx = random.randint(3, 14-size)
        vy = random.randint(3, 14-size)

        self.asteroid_sprites.add(Asteroid(size, posx, posy, vx, vy))

    def update(self):
        self.asteroid_sprites.update()
        self.missile_sprites.update()
        self.player.update()

    def draw(self, screen):
        self.asteroid_sprites.draw(screen)
        self.missile_sprites.draw(screen)
        self.player.draw(screen)


# Where the assets should come from
assets_folder = Path("./assets/")

# Sprite images
asteroid_art = []
for image in (assets_folder / "asteroids").glob("*.png"):
    asteroid_art.append(image.as_posix())


class Missile(pg.sprite.Sprite):
    def __init__(self, xpos, ypos, xvel, yvel):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load((assets_folder / "missile.png").as_posix()).covert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.vx = xvel
        self.vy = yvel

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0


class Asteroid(pg.sprite.Sprite):
    def __init__(self, size, xpos, ypos, xvel, yvel):
        pg.sprite.Sprite.__init__(self)
        # Size is essentially the width, times 10px
        self.image = pg.transform.smoothscale(
                    pg.image.load(random.choice(asteroid_art)).convert(), (30 * size, 30*size))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.vx = xvel
        self.vy = yvel
        self.size = size

    def split(self):
        shards = []
        if self.size <= 1:
            return shards
        else:
            split_into = random.choices([1, 2, 3, 4], [5, 10, 2, 1])
            for i in range(split_into):
                shards.append(
                    Asteroid(self.size-1, self.rect.x, self.rect.y,
                             self.vx + random.randint(0, 2), self.vy + random.randint(0, 2))
                )
            return shards

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

