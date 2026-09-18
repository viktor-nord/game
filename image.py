import pygame


class Image(pygame.sprite.Sprite):
    def __init__(self, src, parent=None, scale=1, size=None, shadow=False):
        super().__init__()
        img = pygame.image.load(src).convert_alpha()
        s = (size, size) if size else (
            img.get_width() * scale, img.get_height() * scale)
        self.image = pygame.transform.scale(img, s)
        if parent:
            self.rect = self.image.get_rect(center=parent.center)
        else:
            self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.surf = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA).convert_alpha()
        if shadow:
            shadow_surf = add_shadow(self.image)
            self.surf.blit(shadow_surf, (0, 0))
        self.surf.blit(self.image, (0, 0))

    def move(self, pos):
        self.rect.center = pos

    def get_shadow_surf(self, img, scale=1.1, offset=2):
        w, h = img.get_width(), img.get_height()
        shadow = pygame.Surface((w * scale, h * scale),
                                pygame.SRCALPHA).convert_alpha()
        while scale > 1:
            scaled_img = pygame.transform.scale(img, (w * scale, h * scale))
            shadow_mask = pygame.mask.from_surface(scaled_img).to_surface(
                setcolor=(0, 0, 0, 3), unsetcolor=None)
            shadow.blit(shadow_mask, shadow_mask.get_rect(
                center=(w / 2 + offset, h / 2 + offset)))
            scale -= 0.01
        return shadow


def add_shadow(img, offset=4):
    shadow_size = 16
    wh = (img.get_width()+shadow_size*2, img.get_height()+shadow_size*2)
    surf = pygame.Surface(wh, pygame.SRCALPHA).convert_alpha()
    c = surf.get_rect().center
    img_rect = img.get_rect(center=c)
    shadow = pygame.mask.from_surface(img).to_surface(
        setcolor=(0, 0, 0, 10),
        unsetcolor=None
    )
    for x in range(16):
        i = pygame.transform.scale(
            shadow, (img_rect.width+x*2, img_rect.height+x*2))
        surf.blit(i, (i.get_rect(center=(c[0]+offset, c[1]+offset))))
    surf.blit(img, (img.get_rect(center=(c[0], c[1]))))
    return surf
