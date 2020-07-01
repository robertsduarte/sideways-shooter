class Settings:
    """Class to store all settings for the game."""
    def __init__(self):
        # Screen attributes
        self.screen_w, self.screen_h = 1280, 720
        self.bg_color = (0, 0, 0)
        
        # Ship attributes
        self.ship_limit = 3

        # Bullet attributes
        self.bullet_w, self.bullet_h = 25, 3
        self.bullet_color = (255, 249, 87)
        self.bullets_allowed = 5

        # Ascending speed scale
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        # Ship attributes
        self.ship_speed = 2.5

        # Bullet attributes
        self.bullet_speed = 7.0

        # Alien attributes
        self.alien_x_speed = -2.5 # default -5.0
        self.alien_y_speed =  0.8 # default 5.0

        # Fleet attributes
        self.fleet_direction = 1 # 1 = down, -1 = up

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed    *= self.speedup_scale
        self.bullet_speed  *= self.speedup_scale
        self.alien_x_speed *= self.speedup_scale
        self.alien_y_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
