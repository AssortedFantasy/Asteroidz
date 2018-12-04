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
score_screen.textBoxes.append(menus.Text("0", 0.48, 0.27, 65))
score_screen.add_button(menus.ButtonSprite('Back', 0.5, 0.5, 250, 80, Path("./Assets/").glob("Back*")))
score_display = menus.Text("", 0, 0.2, 20)
asteroids_display = menus.Text("", 0, 0.3, 20)

state = "MENU"
score = 0
run_game = True

level = 1


def initialize_game(i):
    new_game = asteroids.Game()
    for _ in range(i):
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
            game = initialize_game(1)

        game.health_bar.update_health(game.player_sprite.health)
        score_display.update_text("Score:  {}".format(score + game.score))
        asteroids_display.update_text("Asteroids:  {}".format(len(game.asteroid_sprites.sprites())))
        game.update()
        game.draw(screen)
        screen.blit(score_display.image, (0, 30))
        screen.blit(asteroids_display.image, (0, 55))

        if not game.is_running:
            if game.won:
                level += 1
                score += game.score
                game = initialize_game(level)
            else:
                state = "GAME_OVER"
                score += game.score
                score_screen.textBoxes[0].update_text("{}".format(score))
                level = 1
                score = 0
                game = None

    pg.display.flip()
    clock.tick(fps)
