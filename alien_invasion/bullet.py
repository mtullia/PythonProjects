import pygame
from pygame.sprite import  Sprite

class Bullet(Sprite):
    """A CLASS TO MANAGE BULLETS FIRED FROM THE SHIP"""

    def __init__(self, ai_game):
        """CREATE A BULLET OBJECT AT THE SHIP'S CURRENT POSITION"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #CREATE A BULLET RECT AT (0, 0) AND THEN SET CORRECT POSITION
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #STORE THE BULLET'S POSITION AS A FLOAT
        self.y = float(self.rect.y)
    
    def update(self):
        """MOVE THE BULLET UP THE SCREEN"""
        #UPDATE THE EXACT POSITION OF THE BULLET
        self.y -= self.settings.bullet_speed
        #UPDATE THE RECT POSITION
        self.rect.y = self.y

    def draw_bullet(self):
        """DRAW THE BULLET TO THE SCREEN"""
        pygame.draw.rect(self.screen, self.color, self.rect)