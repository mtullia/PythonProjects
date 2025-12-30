class Settings:
    """ A CLASS TO STORE ALL SETTINGS FOR GAME """
    
    def __init__(self):
        """ INITIALIZE THE GAME'S STATIC SETTINGS """
        #SCREEN SETTINGS
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #SHIP SETTINGS
        self.ship_limit = 3

        #BULLET SETTINGS
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 20

        #ALIEN SETTINGS
        self.fleet_drop_speed = 10

        #HOW QUICKLY THE GAME SPEEDS UP
        self.speedup_scale = 1.5
        #RATE OF ALIEN POINTS VALUES INCREASE
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ INITIALIZE SETTINGS THAT CHANGE THROUGHOUT THE GAME """
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        
        # FLEET_DIRECTION OF 1 REPRESENTS RIGHT; -1 REPRESENTS LEFT
        self.fleet_direction = 1

        #SCORE SETTINGS
        self.alien_points = 50

    def increase_speed(self):
        """ INCREASE SPEED SETTINGS AND ALIEN POINT VALUES"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)