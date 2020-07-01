import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class that represents a single alien in the fleet."""
    def __init__(self, main_class):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.alien_path = 'img/alien.png'
        self.settings = main_class.settings
        self.screen = main_class.screen
        self.screen_rect = self.screen.get_rect()

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load(self.alien_path)
        self.rect = self.image.get_rect()

        # Start each new alien near the top right of the screen
        self.rect.right = self.screen_rect.width
        self.rect.top = 0

        # Store the alien's exact vertical position
        self.y = self.rect.y

        # Wait to move left
        self.move_left_counter = 0

    def check_edges(self):
        """Return True if alien hits edge of the screen."""
        if self.rect.bottom >= self.screen_rect.bottom or self.rect.centery <= 60:
            return True

    def update(self):
        self.y += (self.settings.alien_y_speed * self.settings.fleet_direction)
        self.rect.y = self.y
