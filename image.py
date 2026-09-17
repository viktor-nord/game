import pygame

class Image(pygame.sprite.Sprite):
    def __init__(self, src, parent=None, scale=1, size=None, shadow=False):
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
        if shadow:
            shadow_surf = add_shadow(self.image)
            self.surf.blit(shadow_surf, (0,0))
        self.surf.blit(self.image, (0,0))

    def move(self, pos):
        self.rect.center = pos

    def get_shadow_surf(self, img, scale=1.1, offset=2):
        w, h = img.get_width(), img.get_height()
        shadow = pygame.Surface((w * scale, h * scale), pygame.SRCALPHA).convert_alpha()
        while scale > 1:
            scaled_img = pygame.transform.scale(img, (w * scale, h * scale))
            shadow_mask = pygame.mask.from_surface(scaled_img).to_surface(setcolor=(0,0,0,3), unsetcolor=None)
            shadow.blit(shadow_mask, shadow_mask.get_rect(center = (w / 2 + offset, h / 2 + offset)))
            scale -= 0.01
        return shadow

def add_shadow(img, scale=1.1, offset=2):
    w, h = img.get_width(), img.get_height()
    shadow = pygame.Surface((w * scale, h * scale), pygame.SRCALPHA).convert_alpha()
    while scale > 1:
        scaled_img = pygame.transform.scale(img, (w * scale, h * scale))
        shadow_mask = pygame.mask.from_surface(scaled_img).to_surface(setcolor=(0,0,0,3), unsetcolor=None)
        shadow.blit(shadow_mask, shadow_mask.get_rect(center = (w / 2 + offset, h / 2 + offset)))
        scale -= 0.01
    return shadow
