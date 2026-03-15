import pygame
from random import randrange
from settings import Settings

class D20:
    def __init__(self, dice=20):
        self.img = pygame.image.load("assets/d20.png").convert_alpha()
        self.value = "X"
        self.dice_max_value = dice
        self.x = Settings().screen_width // 2
        self.y = Settings().screen_height // 2
        self.render_img(self.value)
        self.counter = 0
        self.animation_active = True

    def render_img(self, val):
        r = self.img.get_rect()
        self.surf = pygame.Surface((r.width, r.height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surf.get_rect(center = (self.x, self.y))
        self.font = pygame.font.SysFont(None, 32)
        self.text = self.font.render(str(val), True, (239, 239, 239)).convert_alpha()
        img_center = (self.rect.width / 2, self.rect.height / 2 - 4)
        self.text_rect = self.text.get_rect(center = img_center)
        self.surf.blit(self.img, (0,0))
        self.surf.blit(self.text, self.text_rect)

    def blitme(self, screen):
        if self.animation_active:
            frame = self.counter // 5
            deg = frame * 30
            s = pygame.transform.rotate(self.surf, deg)
            r = s.get_rect(center = (self.x, self.y))
            self.counter += 1
            if deg >= 360:
                self.value = randrange(1, self.dice_max_value + 1)
                self.animation_active = False
                self.counter = 0
            screen.blit(s, r)
        else:
            self.render_img(self.value)
            screen.blit(self.surf, self.rect)
