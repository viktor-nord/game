import pygame


class Image(pygame.sprite.Sprite):
    def __init__(self, src, parent=None, scale=1, size=None, shadow_dir=False):
        super().__init__()
        img = pygame.image.load(src).convert_alpha()
        s = (size, size) if size else (
            img.get_width() * scale, img.get_height() * scale)
        self.image = pygame.transform.scale(img, s)
        self.rect = self.create_rect(parent)
        self.width = self.rect.width
        self.height = self.rect.height
        self.surf = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.create_shadow(shadow_dir)
        self.surf.blit(self.image, (0, 0))

    def create_rect(self, parent):
        if parent:
            return self.image.get_rect(center=parent.center)
        else:
            return self.image.get_rect()

    def create_shadow(self, shadow_dir):
        if shadow_dir:
            shadow_surf = add_shadow(self.image, dir_right=False)
            self.surf.blit(shadow_surf, (0, 0))

    def move(self, pos):
        self.rect.center = pos

def add_shadow(img, offset=4, dir_right=True):
    shadow_size = 16
    offset = offset if dir_right else offset * -1
    wh = (img.get_width()+shadow_size*2, img.get_height()+shadow_size*2)
    surf = pygame.Surface(wh, pygame.SRCALPHA).convert_alpha()
    c = surf.get_rect().center
    img_rect = img.get_rect(center=c)
    shadow = pygame.mask.from_surface(img).to_surface(
        setcolor=(0, 0, 0, 10),
        unsetcolor=None
    )
    for x in range(16):
        i = pygame.transform.scale(shadow, (
            img_rect.width + x * 2, img_rect.height + x * 2
        ))
        surf.blit(i, (i.get_rect(center=(c[0]+offset, c[1]+offset))))
    surf.blit(img, (img.get_rect(center=(c[0], c[1]))))
    return surf

def get_title_holder(width):
    # def render_action_pannel_bg(self, url, steps):
    url = 'assets/ui_sprites/Sprites/Content/'
    start = Image(url + '5 Holders/26.png')
    middle = Image(url + '5 Holders/27.png')
    end = Image(url + '5 Holders/28.png')
    # width = 98 if steps < 11 else 108
    wh = (start.width + width + end.width, start.height)
    surf = pygame.Surface(wh, pygame.SRCALPHA).convert_alpha()
    rect = surf.get_rect()
    surf.blit(start.image, (0,0))
    x = start.width
    surf.blit(middle.image, (x, 0))
    while x < width:
        x += middle.width
        surf.blit(middle.image, (x, 0))
    surf.blit(
        end.image, end.image.get_rect(right = rect.width)
    )
    return {'surf': surf, 'rect': rect}