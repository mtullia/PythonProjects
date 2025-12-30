import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """ Overall class to manage game assets and behavior. """

    def __init__(self):
        """ Initialize game and create game resources. """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #CREATE INSTANCE TO STORE GAME STATISTICS 
        # & CREATE A SCOREBOARD
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #START ALIEN INVASION IN AN INACTIVE STATE
        self.game_active = False

        #MAKE THE PLAY BUTTON
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game. """
        while True:
            self._check_events()
                
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """RESPOND TO KEYPRESSES AND MOUSE EVENTS"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            
            #MOVING THE SHIP RIGHT/LEFT, W/ CONTINUOUS MOTION
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_play_button(self, mouse_pos):
        """START A NEW GAME WHEN THE PLAYER CLICKS PLAY"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_active:
            #RESET THE GAME SETTINGS
            self.settings.initialize_dynamic_settings()
            
            #RESET THE GAME STATISTICS
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships
            self.game_active = True
        
            #GET RID OF ANY REMAINING BULLETS AND ALIENS
            self.bullets.empty()
            self.aliens.empty()

            #CREATE A NEW FLEET AND CENTER THE SHIP
            self._create_fleet()
            self.ship.center_ship()

            #HIDE THE MOUSE CURSOR
            pygame.mouse.set_visible(False)
                
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """CREATE A NEW BULLET AND ADD IT TO THE BULLETS GROUP"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """UPDATE POSITION OF BULLETS AND GET RID OF OLD BULLETS"""
        #UPDATE BULLET POSITIONS
        self.bullets.update()
        
        #GET RID OF BULLETS THAT HAVE DISAPPEARED
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """RESPOND TO BULLET-ALIEN COLLISIONS"""
        #REMOVE COLLIDING ALIENS AND BULLETS
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # DESTROY EXISTING BULLETS AND CREATE NEW FLEET
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #INCREASE LEVEL
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """UPDATE THE POSITIONS OF ALL ALIENS IN THE FLEET"""
        self._check_fleet_edges()
        self.aliens.update()

        #LOOK FOR ALIEN/SHIP COLLISIONS
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        #LOOK FOR ALIENS HITTING THE BOTTOM OF THE SCREEN
        self._check_aliens_bottom()
    
    def _check_aliens_bottom(self):
        """CHECK IF ANY ALIENS HAVE REACHED THE BOTTOM OF THE SCREEN"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #TREAT THIS THE SAME AS IF THE SHIP GOT HIT
                self._ship_hit()
                break

    def _create_fleet(self):
        """CREATE THE FLEET OF ALIENS"""
        # MAKE AN ALIEN AND KEEP ADDING ALIENS UNTIL THERE'S NO ROOM LEFT
        # SPACING BETWEEN = 1 ALIEN
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
        
            # FINISHED A ROW; RESET X VALUE, AND INCREMENT Y VALUE
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
        """CREATE AN ALIEN AND PLACE IT IN THE ROW"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _check_fleet_edges(self):
        """RESPOND APPROPRIATELY IF ANY ALIENS HAVE REACHED AN EDGE"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """DROP THE ENTIRE FLEET AND CHANGE THE FLEET'S DIRECTION"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _ship_hit(self):
        """RESPOND TO SHIPS BEING HIT BY ALIEN"""
        if self.stats.ships_left > 0:
            #DECREMENT SHIPS_LEFT, AND UPDATE SCOREBOARD
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #GET RID OF ANY REMAINING BULLETS AND ALIENS
            self.bullets.empty()
            self.aliens.empty()

            #CREATE A NEW FLEET AND CENTER THE SHIP
            self._create_fleet()
            self.ship.center_ship()

            #PAUSE
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """UPDATE IMAGES ON THE SCREEN, AND FLIP TO THE NEW SCREEN"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        #DRAW THE SCORE INFORMATION
        self.sb.show_score()

        #DRAW THE PLAY BUTTON IF THE GAME IS INACTIVE
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()