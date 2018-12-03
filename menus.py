import pygame
from pathlib import Path


class Menu:
    def __init__(self, game_state, bg_path="./assets/Background.png"):
        self.buttons = []
        self.game = game_state
        self.width, self.height = game_state.main_display.get_size()
        self.menu_sprites = pygame.sprite.Group()
        background_location = Path(bg_path)
        try:
            background_file = open(background_location, mode="rb")
        except FileNotFoundError:
            background_file = None
            print("Error: Missing main menu picture! Is the assets folder missing or path incorrect?"
                  "\nPATH={}".format(background_location))
            exit(-1)
        self.menu = pygame.Surface.convert(pygame.image.load(background_file))
        self.original_dim = self.menu.get_size()
        self.menu = pygame.transform.scale(self.menu, self.game.main_display.get_size())
        self.update()

    # Draws the button again
    def update(self):
        for button in self.buttons:
            gx, gy = self.game.main_display.get_size()
            button.rect.center = (gx * button.rel_x, gy * button.rel_y)
            print(button.rect.center)
        self.menu_sprites.update()
        self.menu_sprites.draw(self.menu)
        self.game.main_display.blit(self.menu, (0, 0))

    # Adds a button to the menu and updates the menu
    def add_button(self, button):
        self.buttons.append(button)
        self.update()

    # Returns the name of a button in the menu if it is clicked
    def is_clicked(self):
        for event in self.game.event_queue:
            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        return button.name

class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, name, rel_x, rel_y, width, height, text="", button_colour=(255, 255, 255), text_colour=(0,0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.button_colour = button_colour
        self.text_colour = text_colour
        self.name = name
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.text = " " + text + " "
        pygame.font.init()
        self.font = pygame.font.SysFont("impact", width // len(self.text))
        self.image = self.font.render(self.text, False, self.button_colour, self.text_colour)
        self.rect = self.image.get_rect()
