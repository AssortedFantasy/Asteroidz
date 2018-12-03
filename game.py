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
game = None

run_game = True
state = "MENU"


def initialize_game():
    new_game = asteroids.Game()
    new_game.add_random_asteroid()
    new_game.add_random_asteroid()
    new_game.add_random_asteroid()
    return new_game

while run_game:
    menu = menus.Menu(screen)
    mouse_up = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_game = False
        if event.type == pg.KEYDOWN:
            state = "GAME"
        if event.type == pg.MOUSEBUTTONUP:
            mouse_up = True

    screen.fill((0, 0, 0))

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
        pass
    elif state == "GAME":
        if game is None:
            game = initialize_game()

        game.update()
        game.draw(screen)

    pg.display.flip()
    clock.tick(fps)
