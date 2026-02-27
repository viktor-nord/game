import pygame
from font import PlainText

class ActionWheel:
    def __init__(self):
        self.target_rect = pygame.Rect((0,0),(0,0))
        self.options = ['melee', 'spell', 'move', 'items', 'bonus', 'dash', 'talk', 'other']
        self.actions_db = {
            'primary': {'slot': 1, 'icon': 1, 'pos': (28, -66)},
            'secondary': {'slot': 8, 'icon': 2, 'pos': (-28, -66)},
            'spell': {'slot': 2, 'icon': 3, 'pos': (66, -28)},
            'items': {'slot': 7, 'icon': 4, 'pos': (-66, -28)},
            'range': {'slot': 3, 'icon': 5, 'pos': (66, 28)},
            'dash': {'slot': 6, 'icon': 6, 'pos': (-66, 28)},
            'talk': {'slot': 4, 'icon': 7, 'pos': (28, 66)},
            'other': {'slot': 5, 'icon': 8, 'pos': (-28, 66)}
        }
        self.actions = []
        self.load_images()
        self.image = pygame.Surface((self.base_rect.width, self.base_rect.height), pygame.SRCALPHA).convert_alpha()
        self.image.blit(self.base_image, (0,0))
        self.rect = self.image.get_rect(center = self.target_rect.center)
        self.active_option = ''
        self.action = ''

    def load_images(self):
        url = "assets/ui_sprites/ActionWheel/"
        curl = "assets/ui_sprites/Sprites/Content/"
        self.base_image = get_image(f"{url}aw_base.png", 2)
        self.base_rect = self.base_image.get_rect(center = self.target_rect.center)
        self.holder_image = get_image(f"{curl}5 Holders/24.png")
        self.actions = []
        for key, val in self.actions_db.items():
            self.actions.append(WheelAction(key, val['slot'], val['icon'], val['pos'], self.target_rect))

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.active_option = ''
            for a in self.actions:
                val = a.check_hover(pos)
                if val:
                    self.active_option = val

    def change_target(self, character):
        self.target_rect = character.rect
        self.rect = self.image.get_rect(center = self.target_rect.center)
        self.load_images()

    def handle_click(self, pos=None):
        pos = pos if pos else pygame.mouse.get_pos()
        val = None
        for a in self.actions:
            val = a.check_click(pos)
            if val:
                self.action = val
        return val

    def blitme(self, screen):
        screen.blit(self.image, self.rect)
        for a in self.actions:
            a.blitme(screen)
        if self.active_option:
            t = PlainText(self.active_option)
            screen.blit(t.image, t.image.get_rect(center=self.target_rect.center))

class WheelAction:
    def __init__(self, value, index, icon, pos, target_rect):
        url = "assets/ui_sprites/Sprites/Content/"
        holder_image = get_image(f"{url}5 Holders/24.png")
        icon = get_image(f"{url}1 Items/{icon}.png")
        self.value = value
        self.surf = pygame.Surface((holder_image.get_width(), holder_image.get_height()), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surf.get_rect(center = (target_rect.centerx + pos[0], target_rect.centery + pos[1]))
        self.surf.blit(holder_image, (0,0))
        self.surf.blit(icon, (8,8))
        self.hover_img = get_image(f"assets/ui_sprites/ActionWheel/aw_{index}.png", 2)
        self.is_hover = False
        self.hover_rect = self.hover_img.get_rect(center = target_rect.center)

    def blitme(self, screen):
        screen.blit(self.surf, self.rect)
        if self.is_hover:
            screen.blit(self.hover_img, self.hover_rect)

    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.is_hover = True
            return self.value
        else:
            self.is_hover = False

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return self.value
        else:
            return None

def get_image(src, scale=1):
    base = pygame.image.load(src).convert_alpha()
    return pygame.transform.scale(base, (base.get_width() * scale, base.get_height() * scale))
