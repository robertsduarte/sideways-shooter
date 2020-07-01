import pygame.font

class Button:
    def __init__(self, main_class, msg):
        """Initialize button attributes."""
        self.screen = main_class.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimension and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (30, 30, 150)
        self.text_color = (244, 244, 244)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Msg needs to be prepped only once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and set its position."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw button's background and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
