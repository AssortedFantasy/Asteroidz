import pygame
from pathlib import Path


class Menu:
    def __init__(self, screen, bg_path="./assets/Background.png"):
        self.buttons = []
        self.textBoxes = []
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.menu_sprites = pygame.sprite.Group()
        background_location = Path(bg_path)
        try:
            background_file = open(background_location, mode="rb")
        except FileNotFoundError:
            background_file = None
            print("Error: Missing main menu picture! Is the assets folder missing or path incorrect?"
                  "\nPATH={}".format(background_location))
            exit(-1)
        # Convert image surface so it can blit faster
        self.menu = pygame.Surface.convert(pygame.image.load(background_file))
        # Scale it to the correct resolution
        self.menu = pygame.transform.smoothscale(self.menu, screen.get_size())
        self.update()

    # Draws the button again
    def update(self):
        for button in self.buttons:
            gx, gy = self.screen.get_size()
            button.rect.center = (gx * button.rel_x, gy * button.rel_y)
        for textBox in self.textBoxes:
            gx, gy = self.screen.get_size()
            self.menu.blit(textBox.image, (gx * textBox.rel_x, gy * textBox.rel_y))
        self.menu_sprites.update()
        self.menu_sprites.draw(self.menu)
        self.screen.blit(self.menu, (0, 0))

    # Adds a button to the menu and updates the menu
    def add_button(self, button):
        self.buttons.append(button)
        self.menu_sprites.add(button)
        self.update()

    # Returns the name of a button in the menu if it is clicked
    def is_clicked(self, mouse_pos):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                return button.name

    def is_mouse_over(self):
        for button in self.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.image = button.images[1]
            else:
                button.image = button.images[0]
        self.update()


class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, name, rel_x, rel_y, width, height, button_images, text=""):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.images = []
        self.image_counter = 0
        self.rel_x = rel_x
        self.rel_y = rel_y
        button_image_files = []
        try:
            for image in button_images:
                image_path = Path(image)
                button_image_files.append(open(image_path, mode="rb"))
        except FileNotFoundError:
            button_image_files[-1] = None
            print("Error: Missing main menu picture! Is the assets folder missing or path incorrect?"
                  "\nPATH={}".format(button_images[len(button_image_files) - 1]))
            exit(-1)
        for image in button_image_files:
            self.images.append(pygame.transform.smoothscale(pygame.image.load(image), (width, height)))
        self.image = self.images[self.image_counter]
        self.rect = self.image.get_rect()


class Text:

    def __init__(self, text, rel_x, rel_y, size, text_colour=(255, 255, 255), bg_colour=(0, 0, 0)):
        self.text = " " + text + " "
        self.rel_x = rel_x
        self.rel_y = rel_y
        pygame.font.init()
        self.font = pygame.font.SysFont("impact", size)
        self.image = self.font.render(self.text, True, text_colour, bg_colour)

    def update_text(self, text, text_colour=(255, 255, 255), bg_colour=(0, 0, 0)):
        self.text = " " + text + " "
        self.image = self.font.render(self.text, True, text_colour, bg_colour)
