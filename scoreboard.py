import pygame.font
from pygame.sprite import Group
from lives import Lives

class Scoreboard:
    """A class to report scoring information."""
    def __init__(self, main_class):
        """Initialize scorekeeping attributes."""
        self.main_class = main_class
        self.screen = main_class.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = main_class.settings
        self.stats = main_class.stats
        # Font setting for scoring information.
        self.text_color = (80, 80, 80)
        self.font = pygame.font.SysFont(None, 40)
        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx + self.screen_rect.centerx / 2
        self.score_rect.top = 10

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx-self.screen_rect.centerx/5
        self.high_score_rect.top = 10

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 10
        self.level_rect.top = 10

    def prep_lives(self):
        """Show how many lives are left."""
        self.lives = Group()
        for life_num in range(self.stats.ships_left):
            life = Lives(self.main_class)
            life.rect.x = 15 + life_num * life.rect.width
            life.rect.y = 15
            self.lives.add(life)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw scores and level to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.lives.draw(self.screen)
