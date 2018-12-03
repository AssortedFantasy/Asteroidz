import pygame as pg
import asteroids

WIDTH, HEIGHT = RES = (1280, 720)
fps = 60
speed = 0.1

# Inititalize pygame and create a window
pg.init()
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()


run_game = True
state = "MENU"


def initialize_game():
    sprites = pg.sprite.Group()
    sprites.add(asteroids.Asteroid(3, 100, 100, 10, 10))
    return sprites


all_sprites = None

while run_game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_game = False
        if event.type == pg.KEYDOWN:
            state = "GAME"

    screen.fill((0, 0, 0))

    if state == "MENU":
        # Menu Code
        pass
    elif state == "GAME":
        if all_sprites is None:
            all_sprites = initialize_game()

        all_sprites.update()
        all_sprites.draw(screen)
    pg.display.flip()
    clock.tick(fps)