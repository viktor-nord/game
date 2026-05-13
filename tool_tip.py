import pygame
from font import Text

class ToolTip:
    def __init__(self, text, parent):
        self.text = text
        self.parent = parent
        self.img = pygame.image.load("assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Plain/4 Notification/2 - single papper.png")
        self.surf = pygame.Surface((self.img.get_width(), self.img.get_height()), pygame.SRCALPHA)
        self.surf.blit(self.img, self.img.get_rect())
        self.surf_rect = self.surf.get_rect()
        self.text = Text(text, self.surf_rect, size=18)
        self.text2 = Text(text, self.surf_rect, size=18)
        self.text_area = pygame.Rect((24,8),(self.img.get_width() - 24-24, self.img.get_height() - 16))
        self.text.rect.y = 8
        self.text2.rect.y = 24
        self.surf.blit(self.text.image, self.text.rect)
        self.surf.blit(self.text2.image, self.text2.rect)

    def blitme(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.parent.collidepoint(mouse_pos):
            self.surf_rect.x = mouse_pos[0] + 8
            self.surf_rect.y = mouse_pos[1] + 16
            screen.blit(self.surf, self.surf_rect)
