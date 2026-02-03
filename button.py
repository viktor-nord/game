import pygame
from pygame.sprite import Sprite
from font import Text, PlainText
from tool_tip import ToolTip

class Button(Sprite):
    def __init__(self, game, id, text, parent, value, tool_tip=""):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.id = id
        self.value = value
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
        self.has_tool_tip = len(tool_tip) > 0
        if self.has_tool_tip:
            self.tool_tip = ToolTip(game, tool_tip, self.rect)

    def blitme(self, screen):
        if self.is_hover:
            screen.blit(self.surf_active, self.rect)
        else:
            screen.blit(self.surf, self.rect)
        # if self.has_tool_tip and self.rect.collidepoint(pygame.mouse.get_pos()):
        #     self.tool_tip.update()
        
    def blit_tool_tip(self, screen):
        if self.has_tool_tip and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.tool_tip.blitme(screen)

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.is_hover = True
        else:
            self.is_hover = False

    def check_click(self, pos=None):
        pos = pos if pos else pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.is_checked = True
            self.is_selected = True
            return self.id
        else:
            self.is_checked = False
            self.is_selected = False
            return False

# List =  {"id": any, "text": string, "value": any}
class CheckBoxList():
    def __init__(self, game, parent, list, slim=False, multi=False, pre_selected=[], amount=0, disabled=[]):
        self.game = game
        self.parent = parent
        self.multi = multi
        self.slim = slim
        self.pre_selected = pre_selected
        self.amount = amount
        self.disabled = disabled
        self.list = self.get_list(list)
        self.current = self.list[0].id
        self.selected = []
        for x in pre_selected:
            self.selected.append(x)

    def get_list(self, list):
        arr = []
        box = self.parent.copy()
        box.height = 32
        box.width = box.width // 2
        base_x = box.x
        for i, obj in enumerate(list):
            if self.slim:
                is_disabled = True if obj["text"] in self.disabled else False
                arr.append(CheckBoxSlim(self.game, obj["id"], obj["text"], box, obj["value"], pre_selected = self.pre_selected, is_disabled=is_disabled))
            else:
                arr.append(CheckBox(self.game, obj["id"], obj["text"], box, obj["value"]))
            if i % 2 == 0: #Even
                op = 1 if box.x == base_x else -1
                box.x += box.width * op
            else: # Odd
                box.y += 32
        return arr
    
    def update(self):
        for btn in self.list:
            btn.update()

    def multi_select_click(self, pos):
        for btn in self.list:
            if len(self.selected) == self.amount:
                id = btn.check_click(pos)
                if btn.id in self.selected and id:
                    btn.is_checked = False
                    self.selected.remove(id)
            else:
                id = btn.check_click(pos)
                if id:
                    if id in self.selected:
                        self.selected.remove(id)
                        btn.is_checked = False
                    else:
                        self.selected.append(id)
                        btn.is_checked = True
        return self.selected

    def check_click(self, pos=None):
        pos = pos if pos else pygame.mouse.get_pos()
        val = False
        if self.multi:
            val = self.multi_select_click(pos)
        else:
            for btn in self.list:
                id = btn.check_click()
                if id:
                    self.current = id
                    val = btn.value
        return val

    def draw_list(self, screen):
        for button in self.list:
            button.blitme(screen)
        
class CheckBox(Button):
    def __init__(self, game, id, text, parent, value=None, tool_tip="", is_disabled=False):
        super().__init__(game, id, text, parent, value, tool_tip)
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
        while x < self.container.right - 32 - 16:
            self.surf_active.blit(middle, (x, start_rect.top))
            x += middle.get_width()
        self.surf_active.blit(middle, (x - 8, start_rect.top))
        self.surf_active.blit(end, end.get_rect(right = self.container.right - 16))
        self.surf_active.blit(self.text.text, self.text.rect)

    def blitme(self, screen):
        if self.is_hover:
            screen.blit(self.surf_active, self.rect)
        else:
            screen.blit(self.surf, self.rect)
        if self.is_checked:
            screen.blit(self.check_img, self.check_img_rect)
        if self.is_selected:
            screen.blit(self.arrow, self.arrow_rect)

class CheckBoxSlim():
    def __init__(self, game, id, text, parent, value=None, tool_tip="", pre_selected=[], is_disabled=False):
        self.game_screen = game.screen
        self.is_hover = False
        self.is_disabled = is_disabled
        if id in pre_selected:
            self.is_checked = True
        else:
            self.is_checked = False
        if is_disabled:
            text_color = (105, 138, 128)
        else:
            text_color = None
        self.value = value
        self.id = id
        self.height = game.settings.tile_size
        self.surf = pygame.Surface((parent.width, parent.height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surf.get_rect(center = parent.center)
        url = "assets/ui_sprites/Sprites/Content/"
        self.surf_rect = self.surf.get_rect()
        self.check_box_img = pygame.image.load(url + '5 Holders/22.png').convert_alpha()
        self.check_box_img_rect = self.check_box_img.get_rect(centery = self.surf_rect.centery, left = self.surf_rect.left)
        self.check_img = pygame.image.load(url + "2 Icons/5.png").convert_alpha()
        self.x_img = pygame.image.load(url + "2 Icons/8.png").convert_alpha()
        self.check_img_rect = self.check_img.get_rect(centery = self.rect.centery - 1, left = self.rect.left)
        self.container = self.surf.get_rect(left = self.check_box_img.get_width() + 8, width=self.rect.width - self.check_box_img.get_width() - 8)
        self.text = PlainText(text, color=text_color)
        self.fill_surf(is_disabled)

    def fill_surf(self, is_disabled):
        self.surf.blit(self.check_box_img, self.check_box_img_rect)
        if is_disabled:
            self.surf.blit(self.x_img, self.check_box_img_rect.move(-1, 0))
        tr = self.text.text.get_rect(centery = self.container.centery, left = self.container.left)
        self.surf.blit(self.text.text, tr)

    def blitme(self, screen):
        screen.blit(self.surf, self.rect)
        if self.is_checked:
            screen.blit(self.check_img, self.check_img_rect)
        if self.is_hover:
            r = self.text.under_line_img.get_rect(bottom = self.rect.bottom - 4, left = self.rect.left + self.text.text.get_width() // 2)
            screen.blit(self.text.under_line_img, r)

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.is_hover = True
        else:
            self.is_hover = False

    def check_click(self, pos=None):
        if self.is_disabled:
            return False
        pos = pos if pos else pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return self.id
        else:
            return False
