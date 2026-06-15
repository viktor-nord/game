import pygame
from font import Text
from image import Image

class ActionWheel:
    def __init__(self):
        self.target_rect = pygame.Rect((0,0),(0,0))
        self.current_id = ''
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
        self.base = Image("assets/ui_sprites/ActionWheel/aw_base.png", parent=self.target_rect, scale=2)
        self.load_images()
        self.active_option = ''
        self.active_option_text = Text('')
        self.active_option_rect = self.active_option_text.text.get_rect()
        self.action = ''

    def load_images(self):
        self.actions = []
        for key, val in self.actions_db.items():
            self.actions.append(WheelAction(key, val, self.target_rect))

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.base.rect.collidepoint(pos):
            self.active_option = next((a.value for a in self.actions if a.check_hover(pos)), '')
            self.active_option_text = Text(self.active_option, parent=self.base.rect, is_bold=True)
        else:
            self.active_option = ''

    def change_target(self, character):
        self.target_rect = character.rect
        self.base.move(character.rect.center)
        self.current_id = character.id
        self.load_images()

    def handle_click(self, pos=None):
        pos = pos if pos else pygame.mouse.get_pos()
        self.action = next((a.value for a in self.actions if a.check_click(pos)), '')
        val = {
            "id": self.current_id, 
            "val": self.action
        }
        return val

    def blitme(self, screen):
        screen.blit(self.base.surf, self.base.rect)
        for a in self.actions:
            a.blitme(screen)
        if self.active_option:
            screen.blit(self.active_option_text.text, self.active_option_text.rect)

class WheelAction:
    def __init__(self, value, data, target_rect):
        self.value = value
        self.is_hover = False
        url = "assets/ui_sprites/Sprites/Content/"
        parent = pygame.Rect((
            target_rect.center[0] + data['pos'][0], 
            target_rect.center[1] + data['pos'][1]
        ), (1,1))
        base = Image(f"{url}5 Holders/24.png", parent=parent)
        icon = Image(f"{url}1 Items/{data['icon']}.png").image
        self.hover_img = Image(f"assets/ui_sprites/ActionWheel/aw_{data['slot']}.png", scale=2, parent=target_rect)
        self.surf = base.surf
        self.rect = base.rect
        self.surf.blit(icon, (8,8))

    def blitme(self, screen):
        screen.blit(self.surf, self.rect)
        if self.is_hover:
            screen.blit(self.hover_img.image, self.hover_img.rect)

    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.is_hover = True
            return self.value
        else:
            self.is_hover = False
            return None

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return self.value
        else:
            return None
