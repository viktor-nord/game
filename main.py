import sys
import pygame

from settings import Settings
from start_screen import StartScreen
from character_creation import CharacterCreation
from battle import Battle
from over_world import OverWorld

class Main():
    def __init__(self):
        pygame.init()
        self.running = True
        self.game_pause = False
        self.character_creation_active = False
        self.battle_active = True
        self.settings = Settings()
        sw, sh = self.settings.screen_width, self.settings.screen_height
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((sw, sh))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Akavir: God of none')
        self.start_screen = StartScreen(self)
        self.character_creation = CharacterCreation(self)
        self.battle = Battle()
        self.over_world = OverWorld()

    def run(self):
        while self.running:
            self.check_event()
            if self.game_pause:
                if self.character_creation_active:
                    self.character_creation.update()
                else:
                    self.start_screen.update()
            else:
                if self.battle_active:
                    self.battle.update()
                else:
                    self.over_world.update()
            self.update_screen()
            self.clock.tick(60)

    def update_screen(self):
        self.screen.fill((100,100,100))
        if self.game_pause:
            if self.character_creation_active:
                self.character_creation.blitme(self.screen)
            else:
                self.start_screen.blitme(self.screen)
        else:
            if self.battle_active:
                self.battle.blitme(self.screen)
            else:
                self.over_world.blitme(self.screen)
        pygame.display.flip()

    def check_event(self):
        # pygame.event.set_blocked(pygame.MOUSEWHEEL)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                sys.exit()
            elif  event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.game_pause = True                

            if self.game_pause:
                if self.character_creation_active:
                    self.character_creation.handle_event(event)
                else:
                    self.start_screen.handle_event(event)
            else:
                if self.battle_active:
                    self.battle.handle_event(event)
                else:
                    self.over_world.handle_event(event)
                    if self.over_world.start_battle:
                        self.battle_active = True
                        self.over_world.start_battle = False


if __name__ == '__main__':
    game = Main()
    game.run()
    pygame.quit()
    quit()
