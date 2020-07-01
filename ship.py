import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Manage ship."""
    def __init__(self, game_class):
        """Initialize the ship and set its starting position."""
        super().__init__()

        # Getting attributes from game_class
        self.screen = game_class.screen
        self.settings = game_class.settings

        # Getting the screen rectangle
        self.screen_rect = self.screen.get_rect()

        # Getting image and rectangle of the ship
        self.image = pygame.image.load("img/ship.png")
        self.rect = self.image.get_rect()

        # Positioning ship
        self.rect.centery = self.screen_rect.centery
        self.rect.left = 10

        # Movement flags
        self.move_up = False
        self.move_down = False

        # Typecasting int rect.y to float
        self.y = float(self.rect.y)

    def update(self):
        if self.move_up:
            if self.rect.centery > 80:
                self.y -= self.settings.ship_speed
        if self.move_down:
            if self.rect.centery < self.screen_rect.bottom:
                self.y += self.settings.ship_speed
        self.rect.y = self.y
    
    def blit_me(self):
        # Present ship to the screen
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.centery = self.screen_rect.centery
        self.rect.left = 10
        self.y = float(self.rect.y)
