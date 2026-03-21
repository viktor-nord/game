import pygame
from settings import Settings

# types
# 1: top left to right, then down

class FadeAnimation():
    def __init__(self, game, type=1):
        self.game = game
        self.name = 'fade animation'
        self.settings = Settings()
        self.type = type
        self.image = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA).convert_alpha()
        self.space = 64
        self.box_black = pygame.Surface((self.space, self.space)).convert_alpha()
        self.box_black.fill((0,0,0))
        self.box_shade = pygame.Surface((self.space, self.space), pygame.SRCALPHA).convert_alpha()
        self.box_shade.fill((0,0,0))
        self.box_shade.set_alpha(125)
        self.x = 0
        self.y = 0
        self.animation_active = False
        # self.animation_done = False
        self.fade_in = True

    def reset(self):
        self.animation_active = False
        self.fade_in = True
        # self.animation_done = False

    def type_1(self):
        self.image.blit(self.box_black, (self.x, self.y))
        self.image.blit(self.box_shade, (self.x + self.space, self.y))
        self.x += self.space
        if self.x == self.settings.screen_width:
            self.x = 0
            self.y += self.space
        if self.y == self.settings.screen_height:
            self.game.mode = self.game.transition_to
            self.fade_in = False
            self.x = 0
            self.y = 0

    def fade_out(self):
        delay = 6
        current_alpha = self.image.get_alpha()
        alpha = current_alpha - delay if current_alpha - delay > 0 else 0
        self.image.set_alpha(alpha)
        if alpha == 0:
            self.reset()
            self.game.pause_event = False


    def type_2(self):
        pass

    def blitme(self, screen):
        if self.animation_active:
            if self.fade_in:
                self.type_1()
            else:
                self.fade_out()
            screen.blit(self.image, (0, 0))

        # if self.animation_active:
            # if self.animation_done == False:
                # if self.fade_in:
                #     if self.type == 1:
                #         self.type_1()
                #     elif self.type == 2:
                #         self.type_2()
                # else:
                #     self.fade_out()
            # screen.blit(self.image, (0, 0))
