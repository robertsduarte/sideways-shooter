import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from ship_bullet import ShipBullet
from alien import Alien

class Game:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
                (self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption("Sideways Shooter")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.ship_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "PLAY")

    def _create_fleet(self):
        """Create a fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_width = self.ship.rect.width
        
        # Calculate num_aliens_x and num_aliens_y
        free_space_y = self.settings.screen_h - (2 * alien_height)
        num_aliens_y = free_space_y // (2 * alien_height)
        free_space_x = self.settings.screen_w - (3 * alien_width) - ship_width
        num_aliens_x = free_space_x // (3 * alien_width)
        
        for column_num in range(num_aliens_x):
            for alien_num in range(num_aliens_y):
                self._create_alien(alien_num, column_num)

    def _create_alien(self, alien_num, column_num):
        """Create an alien and place it in the column."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.y = alien_height + (2 * alien_height * alien_num) + 40
        alien.rect.y = alien.y
        alien.rect.x = self.settings.screen_w - alien.rect.width + 2 * alien.rect.width
        alien.rect.x -= 2 * alien.rect.width * column_num
        self.aliens.add(alien)

    def run_game(self):
        """Main loop of the game."""
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()
            
    def check_events(self):
        # Look for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        # Reset the game original settings
        self.settings.init_dynamic_settings()
        # Reset the game stats
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_lives()
        self.stats.game_active = True
        # Delete remaining aliens and bullets.
        self.aliens.empty()
        self.ship_bullets.empty()
        # Create a new fleet and reposition the ship
        self._create_fleet()
        self.ship.center_ship()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _check_keydown(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        if self.stats.game_active:
            if event.key == pygame.K_w:
                self.ship.move_up = True
            if event.key == pygame.K_s:
                self.ship.move_down = True
            if event.key == pygame.K_SPACE:
                self._fire_ship_bullet()
        else:
            if event.key == pygame.K_p and not self.stats.game_active:
                self._start_game()

    def _check_keyup(self, event):
        if event.key == pygame.K_w:
            self.ship.move_up = False
        if event.key == pygame.K_s:
            self.ship.move_down = False

    def _fire_ship_bullet(self):
        """Generate new bullet and add it to the ship_bullets group."""
        if len(self.ship_bullets) < self.settings.bullets_allowed:
            new_bullet = ShipBullet(self)
            self.ship_bullets.add(new_bullet)

    def update_bullets(self):
        """Update position of bullets fired from the ship
        and get rid of old bullets."""
        # Update bullet positions
        self.ship_bullets.update()

        # Remove bullets no longer visible on the screen
        for bullet in self.ship_bullets.copy():
            if bullet.rect.left >= self.settings.screen_w:
                self.ship_bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.ship_bullets, self.aliens, 
                True, True, collided = None)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        # Repopulate the fleet
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.ship_bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def update_aliens(self):
        """Check if fleet hits an edge and update position of all aliens in the fleet."""
        self._check_fleet_edges()
        for alien in self.aliens.sprites():
            alien.update()
            alien.move_left_counter += 1
            if alien.move_left_counter > 5:
                alien.rect.x += int(self.settings.alien_x_speed)
                alien.move_left_counter = 0
        # Look for alien-ship collisions
        alien_ship_collision = pygame.sprite.spritecollideany(self.ship, self.aliens)
        if alien_ship_collision:
            self._ship_hit()
        # Look for collisions between alien and left edge of the screen
        self._alien_hit_left_edge()

    def _check_fleet_edges(self):
        """Respond if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.x += int(self.settings.alien_x_speed)
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_lives()
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.ship_bullets.empty()
            # Create a new fleet and reposition the ship to its original place
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _alien_hit_left_edge(self):
        """Check if any aliens have reached the left edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                self._ship_hit()
                break

    def update_screen(self):
        # Update images on the screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blit_me()

        for bullet in self.ship_bullets.sprites():
            bullet.draw_me()

        self.aliens.draw(self.screen)

        # Draw the score information on the screen.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Flip to the new screen
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run_game()
