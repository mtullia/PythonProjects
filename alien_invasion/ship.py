import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A CLASS TO MANAGE THE SHIP"""
    
    def __init__(self, ai_game):
        """INITIALIZE THE SHIP AND SET ITS STARTING POSITION"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # LOAD THE SHIP IMAGE AND GET ITS RECT
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()

        # START EACH NEW SHIP AT THE BOTTOM CENTER OF THE SCREEN
        self.rect.midbottom = self.screen_rect.midbottom

        #STORE A SLOAT FOR THE SHIPS EXACT X POSITION
        self.x = float(self.rect.x)

        #MOVEMENT FLAG; START WITH A SHIP THAT'S NOT MOVING
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """UPDATE THE SHIP'S POSITION BASED ON THE MOVEMENT FLAG"""
        #UPDATE THE SHIPS X VALUE, NOT THE RECT
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        #UPDATE RECT OBJECT FROM SELF.X
        self.rect.x = self.x

    def blitme(self):
        """ DRAW THE SHIP AT IT'S CURRENT LOCATION """
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """CENTER THE SHIP ON THE SCREEN"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)