import pygame as pg
from pathlib import Path
import random

WIDTH, HEIGHT = 1280, 720

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
                    pg.image.load(random.choice(asteroid_art)).convert(), (10 * size, 10*size))
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

