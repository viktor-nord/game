import sys
import pygame
from pytmx.util_pygame import load_pygame

from player import Player
from settings import Settings
from start_screen import StartScreen
from character_creation import CharacterCreation
from map import Map
from npc import Npc

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
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Akavir: God of none')
        self.animations = pygame.sprite.Group()
        self.map = Map()
        self.player = Player(self)
        self.start_screen = StartScreen(self)
        self.character_creation = CharacterCreation(self)
        self.npc = Npc(self)

    def run(self):
        while self.running:
            self.check_event()
            if self.game_pause:
                if self.character_creation_active:
                    self.character_creation.update()
                else:
                    self.start_screen.update()
            else:
                self.player.update()
            self.animations.update()
            self.update_screen()
            self.clock.tick(60)

    def update_screen(self):
        self.screen.fill((100,100,100))
        self.map.blit_all_tiles(self.screen)
        if self.game_pause:
            if self.character_creation_active:
                self.character_creation.blitme(self.screen)
            else:
                self.start_screen.blitme(self.screen)
        else:
            self.screen.blit(self.npc.image, self.npc.rect)
            self.screen.blit(self.player.image, self.player.rect)
        pygame.display.flip()

    def check_event(self):
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
        if key == pygame.K_SPACE:
            self.handle_action(is_down)
        elif key == pygame.K_p:
            self.game_pause = True
        elif key == pygame.K_q:
            sys.exit()
        else:
            self.player.handle_movement(key, is_down)

    def handle_action(self, is_down):
        if is_down:
            self.map.change_state(self.player)

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
