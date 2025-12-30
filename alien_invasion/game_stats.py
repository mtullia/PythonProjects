class GameStats:
    """TRACK STATISTICS FOR ALIEN INVASION"""
    def __init__(self, ai_game):
        """INITIALIZE STATISTICS"""
        self.settings = ai_game.settings
        self.reset_stats()
        #HIGH SCORE SHOULD NEVER BE RESET
        self.high_score = 0
    
    def reset_stats(self):
        """INITIALIZE STATISTICS THAT CAN CHANGE DURING THE GAME"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1