import pygame

class ActionWheel:
    def __init__(self, player_rect):
        self.player_rect = player_rect
        url = "assets/ui_sprites/ActionWheel/"
        base_image = pygame.image.load(url + "base_action_wheel.png").convert_alpha()
        self.base_image = pygame.transform.scale(base_image, (base_image.get_width() * 2, base_image.get_height() * 2))
        self.base_rect = self.base_image.get_rect()
        self.image = pygame.Surface((self.base_rect.width, self.base_rect.height), pygame.SRCALPHA).convert_alpha()
        self.image.blit(self.base_image, (0,0))
        self.rect = self.image.get_rect(center = player_rect.center)
    
    def blitme(self, screen):
        screen.blit(self.image, self.rect)