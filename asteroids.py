import pygame as pg
from pathlib import Path
import random


# Where the assets should come from
assets_folder = Path("./assets/")

# Sprite images
asteroid_art = []
for image in (assets_folder / "images" / "asteroids").glob("*.png"):
    asteroid_art.append(pg.image.load(image).convert())
missile_art = pg.image.load(assets_folder/ "images" / "missile.png").convert()


class Missile(pg.sprite.Sprite):
    def __init__(self, size, xpos, ypos, xvel, yvel):
        pg.sprite.Sprite.__init__(self)
        self.image = missile_art.copy()
        self.rect = self.image.get_rect()

    def update(self):
        pass


class Asteroid(pg.sprite.Sprite):
    def __init__(self, size, xpos, ypos, xvel, yvel):
        pg.sprite.Sprite.__init__(self)
        # Size is essentially the width, times 10px
        self.image = pg.transform.smoothscale(random.choice(asteroid_art), (10 * size, 10*size))
        self.rect = self.image.get_rect()

    def update(self):
        pass

