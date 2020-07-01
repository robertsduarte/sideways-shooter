import pygame
from pygame.sprite import Sprite

class ShipBullet(Sprite):
    """Class to manage bullets fired from the ship."""
    def __init__(self, main_class):
        super().__init__()

        self.settings = main_class.settings
        self.screen =  main_class.screen
        self.color = self.settings.bullet_color

        # Create a bullet and set its initial position
