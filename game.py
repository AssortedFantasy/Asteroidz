import pygame as pg
import asteroids
import menus

WIDTH, HEIGHT = RES = (1280, 720)
fps = 60
speed = 0.1

# Inititalize pygame and create a window
pg.init()
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()


run_game = True
menu = menus.Menu(screen)
state = "MENU"


def initialize_game():
    sprites = pg.sprite.Group()
    sprites.add(asteroids.Asteroid(3, 100, 100, 20, 20))
    return sprites


all_sprites = None

while run_game:
    mouse_up = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_game = False
        if event.type == pg.KEYDOWN:
            state = "GAME"
        if event.type == pg.MOUSEBUTTONUP:
            mouse_up = True

    if state == "MENU":
        menu.is_mouse_over()
        if mouse_up:
            button_state = menu.is_clicked(pg.mouse.get_pos())
        else:
            button_state = None
        if button_state == "New_Game":
            state = "GAME"
            screen.fill((0, 0, 0))
        elif button_state == "Quit":
            pg.event.post(pg.event.Event(pg.QUIT, {}))
    elif state == "GAME":
        if all_sprites is None:
            all_sprites = initialize_game()

        all_sprites.draw(screen)
        pass

    pg.display.flip()
    clock.tick()