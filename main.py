import sys
import pygame

from settings import Settings
from start_screen import StartScreen
from character_creation import CharacterCreation
from battle import Battle
from over_world import OverWorld
from fade_animation import FadeAnimation

class Main():
    def __init__(self):
        pygame.init()
        self.running = True
        # self.game_pause = True
        # self.character_creation_active = False
        # self.battle_active = False
        self.transition_to = ''
        self.pause_event = False
        self.settings = Settings()
        sw, sh = self.settings.screen_width, self.settings.screen_height
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((sw, sh))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Akavir: God of none')
        self.start_screen = StartScreen(self)
        self.character_creation = CharacterCreation(self)
        self.battle = Battle(self)
        self.over_world = OverWorld(self)
        self.fade_animation = FadeAnimation(self)
        self.mode = self.start_screen.name

    def run(self):
        while self.running:
            self.check_event()
            match self.mode:
                case self.character_creation.name:
                    self.character_creation.update()
                case self.start_screen.name:
                    self.start_screen.update()
                case self.battle.name:
                    self.battle.update()
                case self.over_world.name:
                    self.over_world.update()
            self.update_screen()
            self.clock.tick(60)

    def update_screen(self):
        self.screen.fill((100,100,100))
        match self.mode:
            case self.character_creation.name:
                self.character_creation.blitme(self.screen)
            case self.start_screen.name:
                self.start_screen.blitme(self.screen)
            case self.battle.name:
                self.battle.blitme(self.screen)
            case self.over_world.name:
                self.over_world.blitme(self.screen)
            case self.fade_animation.name:
                self.fade_animation.blitme(self.screen)
        # self.character_creation.blitme(self.screen)
        # self.start_screen.blitme(self.screen)
        # self.battle.blitme(self.screen)
        # self.over_world.blitme(self.screen)
        # self.fade_animation.blitme(self.screen)
        pygame.display.flip()

    def fade(self, to):
        self.transition_to = to
        self.pause_event = True
        self.mode = self.fade_animation.name
        self.fade_animation.animation_active = True

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.pause_event: return
            match self.mode:
                case self.character_creation.name:
                    self.character_creation.handle_event(event)
                case self.start_screen.name:
                    self.start_screen.handle_event(event)
                case self.battle.name:
                    self.battle.handle_event(event)
                case self.over_world.name:
                    self.over_world.handle_event(event)
                case self.fade_animation.name:
                    self.fade_animation.handle_event(event)

            # self.character_creation.handle_event(event)
            # self.start_screen.handle_event(event)
            # self.battle.handle_event(event)
            # self.over_world.handle_event(event)

if __name__ == '__main__':
    game = Main()
    game.run()
    pygame.quit()
    quit()
