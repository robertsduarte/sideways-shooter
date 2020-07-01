import pygame
from pygame.sprite import Sprite

class Lives(Sprite):
    """Manage lives icon."""
    def __init__(self, game_class):
        """Initialize the lives icon and set its starting position."""
        super().__init__()

        # Getting attributes from game_class
        self.screen = game_class.screen
        self.settings = game_class.settings

        # Getting the screen rectangle
        self.screen_rect = self.screen.get_rect()

        # Getting image and rectangle of the lives icon
        self.image = pygame.image.load("img/life.png")
        self.rect = self.image.get_rect()

        # Positioning
        self.rect.left = 20
        self.rect.top = 10
