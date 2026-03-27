import sys
import pygame

from settings import Settings
from start_screen import StartScreen
from character_creation import CharacterCreation
from battle import Battle
from over_world import OverWorld
from fade_animation import FadeAnimation
from settings_menu import SettingsMenu

class Main():
    def __init__(self):
        pygame.init()
        self.running = True
        self.transition_to = ''
        self.pause_event = False
        self.settings = Settings()
        sw, sh = self.settings.screen_width, self.settings.screen_height
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((sw, sh))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Akavir: God of none')
        self.mode = 'start_screen'
        self.settings_menu = SettingsMenu(self)
        self.components = {
            'start_screen': StartScreen(self),
            'character_creation': CharacterCreation(self),
            'battle': Battle(self),
            'over_world': OverWorld(self),
        }
        self.fade_animation = FadeAnimation(self)

    def run(self):
        while self.running:
            self.check_event()
            self.components[self.mode].update()
            self.update_screen()
            self.clock.tick(self.settings.fps)

    def update_screen(self):
        self.screen.fill((0, 2, 22))
        self.components[self.mode].blitme(self.screen)
        self.settings_menu.blitme(self.screen)
        if self.fade_animation.animation_active: 
            self.fade_animation.blitme(self.screen)
        pygame.display.flip()

    def fade(self, to):
        self.transition_to = to
        self.pause_event = True
        self.fade_animation.animation_active = True

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.pause_event: 
                pass
            else:
                if self.settings_menu.open == False:
                    self.components[self.mode].handle_event(event)
                self.settings_menu.handle_event(event)

if __name__ == '__main__':
    game = Main()
    game.run()
    sys.exit()
    pygame.quit()
    quit()
