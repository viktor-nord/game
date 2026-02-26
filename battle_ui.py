import pygame

from settings import Settings

class BattleUI():
    def __init__(self):
        self.settings = Settings()
        self.character_display = pygame.Surface((384, 64), pygame.SRCALPHA).convert_alpha()
        self.character_display_rect = self.character_display.get_rect(centerx = self.settings.screen_width / 2)
        img = pygame.image.load("assets/ui_sprites/character/Frame 19.png").convert_alpha()
        self.char_1 = pygame.transform.scale(img, (64, 64))
        self.character_display.blit(self.char_1, (0,0))

    def update(self):
        pass

    def blitme(self, screen):
        screen.blit(self.character_display, self.character_display_rect)

    def handle_action(self):
        pass

    def handle_click(self):
        pass
