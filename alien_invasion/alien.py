from typing import Any
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A CLASS TO REPRESENT A SINGLE ALIEN IN THE FLEET"""

    def __init__(self, ai_game):
        """INITIALIZE THE ALIEN AND SET IT'S STARTING POSITION"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #LOAD THE ALIEN IMAGE AND SET IT'S RECT ATTRIBUTE
        self.image = pygame.image.load('alien.bmp')
        self.rect = self.image.get_rect()

        #START WITH EACH NEW ALIEN NEAR THE TOP LEFT OF THE SCREEN
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #STORE THE ALIENS EXACT HORIZONTAL POSITION
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """RETURN TRUE IF ALIEN IS AT EDGE OF SCREEN"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        """MOVE THE ALIEN TO THE RIGHT OR LEFT"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x