class GameStats:
    """Track statistics for Sideways Shooter."""
    def __init__(self, main_class):
        self.settings = main_class.settings
        self.reset_stats()
        self.game_active = False
        
        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
