from turtle import width
import pygame
from pygame.sprite import Sprite
from font import Text

class Button(Sprite):
    def __init__(self, game, id, text, parent):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.id = id
        self.parent = parent
        self.img_base = pygame.image.load('assets/button.png').convert_alpha()
        self.img_active = pygame.image.load('assets/button_hover.png').convert_alpha()
        self.wh = (
            self.img_base.get_rect().width * 2, 
            self.img_base.get_rect().height * 2
        )
        self.image = pygame.transform.scale(self.img_base, self.wh)
        self.rect = self.image.get_rect(center = parent.center)
        self.text = Text(text, (self.rect.width / 2, self.rect.height / 2))
        # self.image.blit(self.text.text, self.text.rect)

    def blitme(self):
        self.image.blit(self.text.text, self.text.rect)
        self.screen.blit(self.image, self.rect)

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(self.img_active, self.wh)
        else:
            self.image = pygame.transform.scale(self.img_base, self.wh)

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.game.game_pause:
            return self.id
        else:
            return False

class CheckBoxList():
    def __init__(self, game, parent, list):
        self.game = game
        self.parent = parent
        # self.buttons = pygame.sprite.Group()
        self.list = self.get_list(list)

    def get_list(self, list):
        arr = []
        box = pygame.Rect((self.parent.x, self.parent.y), (self.parent.width, self.parent.height))
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
            # if id == 1:
            #     self.character_creation_active = True
            # elif id == 2:
            #     self.game_pause = False


    def draw_list(self):
        for button in self.list:
            button.blitme()
        
class CheckBox(Button):
    def __init__(self, game, id, text, parent):
        super().__init__(game, id, text, parent)
        self.width = 280
        self.height = game.settings.tile_size
        self.id = id
        # self.rect = pygame.Rect(
        #     (parent.x, parent.y), (parent.width, parent.height)
        # )
        self.is_checked = False
        self.is_active = False
        self.surf = pygame.Surface((parent.width, parent.height), pygame.SRCALPHA)
        self.surf_active = pygame.Surface((parent.width, parent.height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center = parent.center)
        self.ref = self.surf.get_rect(top = 0, left = 0)
        url = "assets/ui_sprites/Sprites/Content/"
        self.arrow = pygame.transform.flip(
            pygame.image.load(url + "4 Buttons/Sliced/5.png"), True, False
        ).convert_alpha()
        self.check_box_img = pygame.image.load(url + '5 Holders/22.png').convert_alpha()
        self.start = pygame.image.load(url + '5 Holders/9.png').convert_alpha()
        self.middle = pygame.image.load(url + '5 Holders/10.png').convert_alpha()
        self.end = pygame.image.load(url + '5 Holders/11.png').convert_alpha()
        self.arrow_rect = self.arrow.get_rect(
            left = self.ref.left, centery = self.ref.centery,
        )
        self.check_box_rect = self.check_box_img.get_rect(
            left = self.arrow_rect.right, centery=self.ref.centery,
        )
        self.start_rect = self.start.get_rect(
            left = self.check_box_rect.right, centery=self.ref.centery,
        )
        self.end_rect = self.end.get_rect(
            right=self.ref.right, centery=self.ref.centery
        )
        self.surf_active.blit(self.arrow, self.arrow_rect)
        self.surf_active.blit(self.check_box_img, self.check_box_rect)
        self.surf_active.blit(self.start, self.start_rect)
        self.blit_middle()
        self.surf_active.blit(self.end, self.end_rect)

        text_box = pygame.Rect(self.start_rect.left, self.start_rect.top, self.end_rect.right - self.start_rect.left, self.start_rect.height)
        self.text = Text(text, text_box.center, has_underline=True)
        self.surf.blit(self.text.text, self.text.rect)
        self.surf_active.blit(self.text.text, self.text.rect)

    def blit_middle(self):
        x = self.start_rect.right
        y = self.start_rect.top
        while x < self.ref.right - 16:
            self.surf_active.blit(self.middle, (x,y))
            x += self.middle.get_width()        

    def blitme(self):
        if self.is_active:
            self.screen.blit(self.surf_active, self.rect)
        else:
            self.screen.blit(self.surf, self.rect)

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self.check_collision(self.rect, pos):
            return self.id
        else:
            return False

    def check_collision(self, rect, pos):
        return rect.left <= pos[0] and rect.top <= pos[1] and rect.right >= pos[0] and rect.bottom >=pos[1]
        
    def update(self):
        pos = pygame.mouse.get_pos()
        if self.check_collision(self.rect, pos):
            self.is_active = True
        else:
            self.is_active = False


        
            
