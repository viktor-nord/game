import pygame

class Image(pygame.sprite.Sprite):
    def __init__(self, src, parent=None, scale=1, size=None):
        super().__init__()
        img = pygame.image.load(src).convert_alpha()
        s = (size, size) if size else (img.get_width() * scale, img.get_height() * scale)
        self.image = pygame.transform.scale(img, s)
        if parent:
            self.rect = self.image.get_rect(center = parent.center)
        else:
            self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.surf.blit(self.image, (0,0))

    def move(self, pos):
        self.rect.center = pos