import pygame as pg
import menus

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
    pass


while run_game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_game = False

    if state == "MENU":
        menu = menus.Menu()
        pass
    elif state == "GAME":
        # Game code
        pass
    pg.display.flip()