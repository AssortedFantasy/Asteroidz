import pygame as pg
from pathlib import Path
import asteroids
import menus


# Global Parameters
# Note you need to update WIDTH/HEIGHT in asteroids as well! (Although its not really used very much)
WIDTH, HEIGHT = RES = (1280, 720)
fps = 60

# Inititalize Pygame and create a Display
pg.init()
screen = pg.display.set_mode(RES)
pg.display.set_caption("ASTEROIDZ - CMPUT274 Final Project by Tharidu and Jehanzeb")
clock = pg.time.Clock()

# Menu buttons and Setup
menu = menus.Menu(screen)
menu.add_button(menus.ButtonSprite('New_Game', 0.5, 0.4, 600, 100, Path("./Assets/").glob("New_game*")))
menu.add_button(menus.ButtonSprite('Quit', 0.5, 0.6, 300, 90, Path("./Assets/").glob("Quit*")))
score_screen = menus.Menu(screen, bg_path="./assets/Score_screen.png")
score_screen.textBoxes.append(menus.Text("0", 0.48, 0.27, 65))
score_screen.add_button(menus.ButtonSprite('Back', 0.5, 0.5, 250, 80, Path("./Assets/").glob("Back*")))
score_display = menus.Text("", 0, 0.2, 20)
asteroids_display = menus.Text("", 0, 0.3, 20)
level_display = menus.Text("Level: 1", 0, 0.3, 20)
fps_display = menus.Text("", 0.935, 0, 20)

# The Main loop is setup as a finite state machine, these are some of the variables it uses
game = None
state = "MENU"
score = 0
level = 1
run_game = True
mouse_clicked = False


# This function creates a new game and initializes it with a bunch of Asteroids
def initialize_game(i):
    new_game = asteroids.Game()
    for _ in range(i):
        new_game.add_random_asteroid()
    return new_game


# Main Game loop
while run_game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_game = False
        elif event.type == pg.MOUSEBUTTONUP:
            mouse_clicked = True  # Only where you un press the mouse matters.

    screen.fill((0, 0, 0))

    if state == "MENU":
        menu.is_mouse_over()
        if mouse_clicked:
            button_state = menu.is_clicked(pg.mouse.get_pos())
        else:
            button_state = None
        if button_state == "New_Game":
            state = "GAME"
            screen.fill((0, 0, 0))
        elif button_state == "Quit":
            run_game = False
    elif state == "GAME_OVER":
        score_screen.is_mouse_over()
        if mouse_clicked:
            button_state = score_screen.is_clicked(pg.mouse.get_pos())
            print(button_state)
        else:
            button_state = None
        if button_state == "Back":
            state = "MENU"
            menu.update()
            pass
    elif state == "GAME":
        # When this loop is first called, there is no game at all, this is how it is started.
        if game is None:
            game = initialize_game(level)

        game.health_bar.update_health(game.player_sprite.health)
        score_display.update_text("Score:  {}".format(score + game.score))
        asteroids_display.update_text("Asteroids:  {}".format(len(game.asteroid_sprites.sprites())))
        fps_display.update_text(f"FPS: {clock.get_fps():2.1f}")
        game.update()
        game.draw(screen)
        screen.blit(score_display.image, (0, 55))
        screen.blit(asteroids_display.image, (0, 80))
        screen.blit(level_display.image, (0, 30))
        screen.blit(fps_display.image, (WIDTH * fps_display.rel_x, HEIGHT * fps_display.rel_y))
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
            level_display.update_text(f"Level: {level}")

    pg.display.flip()
    clock.tick(fps)
