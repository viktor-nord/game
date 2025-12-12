import pygame
from pygame.sprite import Sprite
from font import Text

class Button(Sprite):
    def __init__(self, game, id, text, parent):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.id = id
        self.is_hover = False
        self.is_checked = False
        self.is_selected = False
        self.parent = parent
        self.img_base = pygame.image.load('assets/button.png').convert_alpha()
        self.img_active = pygame.image.load('assets/button_hover.png').convert_alpha()
        self.wh = (
            self.img_base.get_rect().width * 2, 
            self.img_base.get_rect().height * 2
        )
        self.surf = pygame.Surface(self.wh, pygame.SRCALPHA)
        self.surf_active = pygame.Surface(self.wh, pygame.SRCALPHA)
        self.image = pygame.transform.scale(self.img_base, self.wh)
        self.surf.blit(pygame.transform.scale(self.img_base, self.wh), (0,0))
        self.surf_active.blit(pygame.transform.scale(self.img_active, self.wh), (0,0))
        self.rect = self.surf.get_rect(center = parent.center)
        self.text = Text(text, self.surf.get_rect())
        self.surf.blit(self.text.image, self.text.rect)
        self.surf_active.blit(self.text.image, self.text.rect)

    def blitme(self):
        if self.is_hover:
            self.screen.blit(self.surf_active, self.rect)
        else:
            self.screen.blit(self.surf, self.rect)

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.is_hover = True
        else:
            self.is_hover = False

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.game.game_pause:
            self.is_checked = True
            self.is_selected = True
            return self.id
        else:
            self.is_checked = False
            self.is_selected = False
            return False

class CheckBoxList():
    def __init__(self, game, parent, list):
        self.game = game
        self.parent = parent
        self.list = self.get_list(list)

    def get_list(self, list):
        arr = []
        box = self.parent.copy()
        box.height = 32
        for i, button in enumerate(list):
            arr.append(CheckBox(self.game, button["id"], button["text"], box))
            box.y += 32
        return arr
    
    def update(self):
        for btn in self.list:
            btn.update()

    def check_click(self):
        for btn in self.list:
            id = btn.check_click()
            print(id)

    def draw_list(self):
        for button in self.list:
            button.blitme()
        
class CheckBox(Button):
    def __init__(self, game, id, text, parent):
        super().__init__(game, id, text, parent)
        # self.width = 280
        self.height = game.settings.tile_size
        self.surf = pygame.Surface((parent.width, parent.height), pygame.SRCALPHA)
        self.surf_active = pygame.Surface((parent.width, parent.height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center = parent.center)
        url = "assets/ui_sprites/Sprites/Content/"
        arrow_img = pygame.image.load(url + "4 Buttons/Sliced/5.png").convert_alpha()
        self.arrow = pygame.transform.flip(arrow_img, True, False)
        self.check_box_img = pygame.image.load(url + '5 Holders/22.png').convert_alpha()
        self.check_img = pygame.image.load(url + "2 Icons/5.png").convert_alpha()
        space = self.arrow.get_width() + self.check_box_img.get_width()
        self.container = self.surf.get_rect(left=space, width=self.rect.width-space)
        self.arrow_rect = self.arrow.get_rect(left=self.rect.left, centery=self.rect.centery)
        self.check_box_rect = self.check_box_img.get_rect(right=self.container.left, centery=self.container.centery)
        self.check_img_rect = self.check_img.get_rect(x = self.rect.x + 16, centery = self.rect.centery - 1)
        text_container = self.container.copy()
        text_container.x += 8
        text_container.y += 6
        self.text = Text(text, text_container, has_underline=True, centered=False)
        self.fill_surf()
        self.fill_active_surf(url)

    def fill_surf(self):
        self.surf.blit(self.check_box_img, self.check_box_rect)
        self.surf.blit(self.text.text, self.text.rect)

    def fill_active_surf(self, url):
        start = pygame.image.load(url + '5 Holders/9.png').convert_alpha()
        middle = pygame.image.load(url + '5 Holders/10.png').convert_alpha()
        end = pygame.image.load(url + '5 Holders/11.png').convert_alpha()
        start_rect = start.get_rect(left = self.container.left - 4)
        self.surf_active.blit(self.check_box_img, self.check_box_rect)
        self.surf_active.blit(start, start_rect)
        x = start_rect.right
        while x < self.container.right - 32:
            self.surf_active.blit(middle, (x, start_rect.top))
            x += middle.get_width()
        self.surf_active.blit(middle, (x - 8, start_rect.top))
        self.surf_active.blit(end, end.get_rect(right = self.container.right))
        self.surf_active.blit(self.text.text, self.text.rect)

    def blitme(self):
        if self.is_hover:
            self.screen.blit(self.surf_active, self.rect)
        else:
            self.screen.blit(self.surf, self.rect)
        if self.is_checked:
            self.screen.blit(self.check_img, self.check_img_rect)
        if self.is_selected:
            self.screen.blit(self.arrow, self.arrow_rect)