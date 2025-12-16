import pygame
from font import Text

class ToolTip:
    def __init__(self, game, text, parent):
        self.game = game
        self.text = text
        self.parent = parent
        self.surf = pygame.Surface((272, 112), pygame.SRCALPHA)
        self.img = pygame.image.load("assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Plain/4 Notification/2 - single papper.png")
        self.surf.blit(self.img, self.img.get_rect())
        # self.surf.blit(self.img, (0, 0))
        self.surf_rect = self.surf.get_rect()
        self.text = Text(text, self.surf_rect, size=18)
        self.text2 = Text(text, self.surf_rect, size=18)
        self.text.rect.y = 40
        self.text2.rect.y = 58
        self.surf.blit(self.text.image, self.text.rect)
        self.surf.blit(self.text2.image, self.text2.rect)
        # self.start_loop()

    def blitme(self, screen):
        # gg=0
        mouse_pos = pygame.mouse.get_pos()
        if True:
        # if self.parent.collidepoint(mouse_pos):
            # print(mouse_pos)
            self.surf_rect.move(mouse_pos)
            self.surf_rect.x = mouse_pos[0] - 8
            self.surf_rect.y = mouse_pos[1] - 16
            screen.blit(self.surf, self.surf_rect)
            # pygame.display.update(self.surf_rect)
