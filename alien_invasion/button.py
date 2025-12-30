import pygame.font

class Button:
    """A CLASS TO BUILD BUTTONS FOR THE GAME"""
    def __init__(self, ai_game, msg):
        """INITIALIZE BUTTON ATTRIBUTES"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #SET THE DIMENSIONS AND PROPERTIES OF THE BUTTON
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #BUILD THE BUTTON'S RECT OBJECT AND CENTER IT
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #THE BUTTON MESSAGE NEEDS TO BE PREPPED ONLY ONCE
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """TURN MSG INTO A RENDERED IMAGE AND CENTER TEXT ON THE BUTTON"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """DRAW BLANK BUTTON AND THEN DRAW MESSAGE"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)