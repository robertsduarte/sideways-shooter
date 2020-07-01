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
        self.rect = pygame.Rect(0, 0, self.settings.bullet_w,
                self.settings.bullet_h)

        self.rect.left = main_class.ship.rect.right - 5
        self.rect.centery = main_class.ship.rect.centery
        # self.rect.midleft = main_class.ship.rect.midright

        # Store bullet's position as decimal
        self.x = float(self.rect.x)

    def update(self):
        # Move bullet to the right of the screen
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_me(self):
        # Draw bullet to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)
