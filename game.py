import pygame as pg
from pathlib import Path
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

menu = menus.Menu(screen)
menu.add_button(menus.ButtonSprite('New_Game', 0.5, 0.4, 600, 100, Path("./Assets/").glob("New_game*")))
menu.add_button(menus.ButtonSprite('Quit', 0.5, 0.6, 300, 90, Path("./Assets/").glob("Quit*")))
score_screen = menus.Menu(screen, bg_path="./assets/Score_screen.png")
score_screen.textBoxes.append(menus.Text("231", 0.48, 0.27, 65))
score_screen.add_button(menus.ButtonSprite('Back', 0.5, 0.5, 250, 80, Path("./Assets/").glob("Back*")))


# state = "MENU"
state = "GAME_OVER"
run_game = True

def initialize_game():
    new_game = asteroids.Game()
    new_game.add_random_asteroid()
    new_game.add_random_asteroid()
    new_game.add_random_asteroid()
    return new_game

while run_game:
    mouse_up = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_game = False
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
    elif state == "GAME_OVER":
        score_screen.is_mouse_over()
        if mouse_up:
            button_state = score_screen.is_clicked(pg.mouse.get_pos())
            print(button_state)
        else:
            button_state = None
        if button_state == "Back":
            state = "MENU"
            menu.update()
            pass
    elif state == "GAME":
        if game is None:
            game = initialize_game()

        if not game.is_running:
            state = "GAME_OVER"

        game.update()
        game.draw(screen)

    pg.display.flip()
    clock.tick(fps)
