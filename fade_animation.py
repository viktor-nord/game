import pygame
from settings import Settings

# types
# 1: top left to right, then down

class FadeAnimation():
    def __init__(self, type=1):
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
        self.animation_done = False
        self.fade_in = True

    def type_1(self):
        self.image.blit(self.box_black, (self.x, self.y))
        self.image.blit(self.box_shade, (self.x + self.space, self.y))
        self.x += self.space
        if self.x == self.settings.screen_width:
            self.x = 0
            self.y += self.space
        if self.y == self.settings.screen_height:
            self.animation_done = True
            self.x = 0
            self.y = 0

    def fade_out(self):
        current_alpha = self.image.get_alpha()
        alpha = current_alpha - 10 if current_alpha - 10 > 0 else 0
        self.image.set_alpha(alpha)
        if alpha == 0:
            self.animation_done = True

    def type_2(self):
        pass

    def blitme(self, screen):
        if self.animation_active:
            if self.animation_done == False:
                if self.type == 1:
                    self.type_1()
                elif self.type == 2:
                    self.type_2()
            screen.blit(self.image, (0, 0))
