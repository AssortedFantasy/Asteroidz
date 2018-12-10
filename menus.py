import pygame
from pathlib import Path


# Class that creates a template for creating and drawing menu screens
class Menu:
    ###
    #
    # Description: Initializes the Menu object
    #
    # Arguments:
    #   self: The Menu object itself
    #   screen: The surface to draw the menu to
    #   bg_path: Path to the background image of the menu
    #
    # Returns: None
    ###
    def __init__(self, screen, bg_path="./assets/Background.png"):
        # List to store button objects
        self.buttons = []
        # List to store text objects
        self.textBoxes = []
        self.screen = screen
        self.width, self.height = screen.get_size()
        # Sprite Group for all sprites used in buttons
        self.menu_sprites = pygame.sprite.Group()
        # The path of the background image for this menu
        # Attempts to safely open either image
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

    ###
    # Description: Updates the sprites and text, and draws them to the screen
    #
    # Arguments: None
    #
    # Returns: None
    ###
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

    ###
    # Description: Adds a button to the menu sprites group and updates the screen
    #
    # Arguments:
    #   button: A button object to be added to the menu sprites
    #
    # Returns: None
    ###
    def add_button(self, button):
        self.buttons.append(button)
        self.menu_sprites.add(button)
        self.update()

    ###
    # Description: Returns the name of a button in the menu if it is clicked
    #
    # Arguments:
    #   mouse_pos: The position of the mouse
    #
    # Returns:
    #   button.name: The name of the button that was clicked, if it was clicked
    ###
    def is_clicked(self, mouse_pos):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                return button.name

    ###
    # Description: Tests if the mouse is over the button and updates the button image to the active image
    #
    # Arguments: None
    #
    # Returns: None
    ###
    def is_mouse_over(self):
        for button in self.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                # Active button image is used
                button.image = button.images[1]
            else:
                # Passive button image is used
                button.image = button.images[0]
        self.update()


# Button class that is sprite based
# Defines a button with relative coordinates
class ButtonSprite(pygame.sprite.Sprite):
    ###
    #
    # Description: Initializes a Button sprite object
    #
    # Arguments:
    #   self: The Button object itself
    #   name: The identifier of the button, intended to be used to determine what to do if the button is clicked
    #   rel_x: A floating point value from 0.0 to 1.0 that defines the x position of the button when
    #          multiplied by the size of the screen that it is being drawn to
    #   rel_y: A floating point value from 0.0 to 1.0 that defines the y position of the button when
    #          multiplied by the size of the screen that it is being drawn to
    #   width: The width of the button
    #   height: The height of the button
    #   button_images: A list of image paths which will be rendered on the button
    #
    # Returns: None
    ###
    def __init__(self, name, rel_x, rel_y, width, height, button_images, text=""):
        pygame.sprite.Sprite.__init__(self)
        # Name of the button, intended to be used to identify which button is pressed
        self.name = name
        # Image array, stores all potential appearances of the button
        self.images = []
        self.image_counter = 0
        # A value from 0 to 1, determines the x coordinate relative to the screen
        self.rel_x = rel_x
        self.rel_y = rel_y
        # List to store the image objects created from opening the list of paths in the button_images list
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
        # Scale each image to the correct width and height and adds it to the images list
        for image in button_image_files:
            self.images.append(pygame.transform.smoothscale(pygame.image.load(image), (width, height)))
        # Sets the sprite image to be the default image_id
        self.image = self.images[self.image_counter]
        self.rect = self.image.get_rect()


# A Class that defines and creates text surfaces
class Text:
    ###
    #
    # Description: Initializes a Button sprite object
    #
    # Arguments:
    #   self: The Button object itself
    #   text: String that stores the text that will be drawn
    #   rel_x: A floating point value from 0.0 to 1.0 that defines the x position of the button when
    #          multiplied by the size of the screen that it is being drawn to
    #   rel_y: A floating point value from 0.0 to 1.0 that defines the y position of the button when
    #          multiplied by the size of the screen that it is being drawn to
    #   size: The font size of the text to be rendered
    #   text_colour: A three value tupple that defines the RGB value of the text, assumed white
    #   text_colour: A three value tupple that defines the RGB value of the background of the text, assumed black
    #   font: The font to be rendered, default is impact
    # Returns: None
    ###
    def __init__(self, text, rel_x, rel_y, size, text_colour=(255, 255, 255), bg_colour=(0, 0, 0)):
        self.text = " " + text + " "
        self.rel_x = rel_x
        self.rel_y = rel_y
        pygame.font.init()
        self.font = pygame.font.SysFont("impact", size)
        self.image = self.font.render(self.text, True, text_colour, bg_colour)
        self.image.set_colorkey((0, 0, 0))

    ###
    #
    #   Description: Changes the text that will be rendered
    #
    #   Arguments:
    #       self: The text object itself
    #       text: The new text to be rendered
    #       text_colour: A three value tupple that defines the RGB value of the text, assumed white
    #       text_colour: A three value tupple that defines the RGB value of the background of the text, assumed black
    ###
    def update_text(self, text, text_colour=(255, 255, 255), bg_colour=(0, 0, 0)):
        self.text = " " + text + " "
        self.image = self.font.render(self.text, True, text_colour, bg_colour)
        self.image.set_colorkey((0, 0, 0))
