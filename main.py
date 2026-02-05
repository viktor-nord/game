import sys
import pygame

from player import Player
from settings import Settings
from start_screen import StartScreen
from character_creation import CharacterCreation
from map import Map

class Main():
    def __init__(self):
        pygame.init()
        self.running = True
        self.game_pause = True
        self.character_creation_active = False
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.SCALED)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Akavir: God of none')
        self.animations = pygame.sprite.Group()
        self.map = Map()
        self.player = Player(self)
        self.start_screen = StartScreen(self)
        self.character_creation = CharacterCreation(self)

    def run(self):
        while self.running:
            self.check_event()
            if self.game_pause:
                self.update_pause_menu()
            else:
                self.update_world()
            self.animations.update()
            self.update_screen()
            self.clock.tick(60)

    def update_pause_menu(self):
        if self.character_creation_active:
            self.character_creation.update()
        else:
            self.start_screen.update()

    def update_world(self):
        self.player.update()

    def update_screen(self):
        self.screen.fill((100,100,100))
        if self.game_pause:
            self.blit_pause_menu()
        else:
            self.blit_world()
        pygame.display.flip()

    def blit_pause_menu(self):
        if self.character_creation_active:
            self.character_creation.blitme(self.screen)
        else:
            self.start_screen.blitme(self.screen)

    def blit_world(self):
        self.map.blit_all_tiles(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.map.blit_overlay(self.player.rect, self.screen)

    def check_event(self):
        pygame.event.set_blocked(pygame.MOUSEWHEEL)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click()
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event.key, True)
            elif event.type == pygame.KEYUP:
                self.handle_key(event.key, False)
    #         elif event.type == pygame.MOUSEWHEEL:
    #             self.handle_scroll(event.y)

    # def handle_scroll(self, y):
    #     scroll_down = True
    #     if y > 0:
    #         scroll_down = False
    #     print(f"scroll_down: {scroll_down}")

    def handle_key(self, key, is_down):
        if self.character_creation.general_page.name_input.is_active or self.character_creation.general_page.age_input.is_active:
            if is_down:
                self.character_creation.handle_key(key)
        elif key == pygame.K_SPACE:
            if is_down:
                self.handle_action()
        elif key == pygame.K_p:
            self.game_pause = True
        elif key == pygame.K_q:
            sys.exit()
        else:
            self.handle_player_movement()

    def handle_player_movement(self):
        not_colliding = self.map.check_collision(self.player.rect)
        if not_colliding:
            self.player.handle_movement()

    def handle_action(self):
        gg=0
        # self.map.change_state((self.player.rect.x, self.player.rect.y))

    def handle_click(self):
        if self.game_pause == False:
            return 
        if self.character_creation_active:
            self.character_creation.handle_click()
        else:
            self.start_screen.handle_click()

if __name__ == '__main__':
    game = Main()
    game.run()
    pygame.quit()
    quit()
