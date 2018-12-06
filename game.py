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

# Initializes the main menu object and adds the apropriate buttons to the ButtonSprite
menu = menus.Menu(screen)
menu.add_button(menus.ButtonSprite('New_Game', 0.5, 0.4, 600, 100, Path("./Assets/").glob("New_game*")))
menu.add_button(menus.ButtonSprite('Quit', 0.5, 0.6, 300, 90, Path("./Assets/").glob("Quit*")))

# Initializes the score_screen object and adds the apropriate buttons to the ButtonSprite
score_screen = menus.Menu(screen, bg_path="./assets/Score_screen.png")
score_screen.textBoxes.append(menus.Text("0", 0.48, 0.27, 65))
score_screen.add_button(menus.ButtonSprite('Back', 0.5, 0.5, 250, 80, Path("./Assets/").glob("Back*")))

# Defines text to be rendered to teh screen burring the game
score_display = menus.Text("", 0, 0.2, 20)
asteroids_display = menus.Text("", 0, 0.3, 20)
level_display = menus.Text("Level: 1", 0, 0.3, 20)
fps_display = menus.Text("", 0.935, 0, 20)

# Sets the initial state
state = "MENU"
score = 0
run_game = True
level = 1

###
#
#   Description: Initializes the game and draws a given number of asteroids
#
#   Arguments:
#       i: Store the initial number of asteroids
#   returns: new_game state
###
def initialize_game(i):
    new_game = asteroids.Game()
    for _ in range(i):
        new_game.add_random_asteroid()
    return new_game


# Infinite loop to run game mode
while run_game:
    # Checks if the mouse has been clicked
    mouse_up = False
    for event in pg.event.get():
        # If the event says to close the window, close the window
        if event.type == pg.QUIT:
            # Sets game_state to be false
            run_game = False
        if event.type == pg.MOUSEBUTTONUP:
            # If the mouse has been clicked
            mouse_up = True

    # Resets screen to black screen to get rid of ghosting trails
    screen.fill((0, 0, 0))

    # If the game is in the menu state, check if menu buttons were pressed, and acts according to the button name
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

        # Updates game display with a health bar, score_display, asteroid count, and pfs display
        game.health_bar.update_health(game.player_sprite.health)
        score_display.update_text("Score:  {}".format(score + game.score))
        asteroids_display.update_text("Asteroids:  {}".format(len(game.asteroid_sprites.sprites())))
        fps_display.update_text(f"FPS: {clock.get_fps():2.1f}")
        # Updates the button sprites of the game
        game.update()
        # Draws the menus and GUI above to the screen and updates the screen in the correct location
        game.draw(screen)
        screen.blit(score_display.image, (0, 55))
        screen.blit(asteroids_display.image, (0, 80))
        screen.blit(level_display.image, (0, 30))
        screen.blit(fps_display.image, (WIDTH * fps_display.rel_x, HEIGHT * fps_display.rel_y))

        # If the level is over
        if not game.is_running:
            # If you won the game
            if game.won:
                level += 1
                score += game.score
                game = initialize_game(level)
            # If you lost the game
            else:
                state = "GAME_OVER"
                score += game.score
                score_screen.textBoxes[0].update_text("{}".format(score))
                level = 1
                score = 0
                game = None
            level_display.update_text(f"Level: {level}")

    # Updates the clock
    pg.display.flip()
    clock.tick(fps)
