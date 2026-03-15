import pygame
import json
from settings import Settings
from font import PlainText
from button import TextButton

class InfoDisplay:
    def __init__(self):
        self.settings = Settings()
        img = pygame.image.load('assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Plain/5 Mini Map/1.png').convert_alpha()
        self.image = pygame.Surface((img.get_width(), img.get_height()), pygame.SRCALPHA).convert_alpha()
        self.go_back_img = pygame.image.load("assets/ui_sprites/Sprites/Content/2 Icons/go_back_arrow.png").convert_alpha()
        self.rect = self.image.get_rect(centery = self.settings.screen_height / 2, right = self.settings.screen_width)
        self.image.blit(img, (0,0))
        # self.container = pygame.Rect((self.rect.x + 50, self.rect.y + 51), (124, 122))
        self.container = pygame.Rect((50, 60), (124, 122))
        self.active = True

    def blitme(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
            # pygame.draw.rect(screen, (0,0,0), self.container)

class MiraclesInfoDisplay(InfoDisplay):
    def __init__(self, miracles):
        super().__init__()
        self.miracles = {
            'cantrips': {},
            'lv1': {},
            'lv2': {},
            'lv3': {},
            'lv4': {},
            'lv5': {},
        }
        self.get_miracles(miracles)
        self.states = ['level', 'select', 'data']
        self.state = 0
        self.sub_state = ''
        self.name = 'Miracles'
        self.con = self.container.move(self.rect.topleft)
        self.title = PlainText("Miracles")
        self.title.rect.centerx = self.rect.centerx
        self.title.rect.y = self.rect.y + 40
        self.go_back_img_rect = self.go_back_img.get_rect(centery = self.title.rect.centery, right = self.title.rect.left - 4)
        self.level_buttons = self.get_lv_buttons(self.con)
        self.miracle_buttons = []
        # self.miracle_name = PlainText('Toll the dead')
        # self.miracle_name.rect.x = self.con.x
        # self.miracle_name.rect.y = self.con.y

    def get_lv_buttons(self, container):
        labels = ['cantrips', 'lv 1', 'lv 2', 'lv 3', 'lv 4', 'lv 5']
        arr = []
        for i, l in enumerate(labels):
            arr.append(TextButton(l, container.move(0, 18 * i)))
        return arr
    
    def get_miracle_buttons(self, container):
        i = 0
        for key, val in self.miracles[self.sub_state].items():
            self.miracle_buttons.append(TextButton(key, container.move(0, 18 * i)))
            i += 1

    def get_info_text(self):
        self.miracle_name = PlainText(self.name)
        self.miracle_name.rect.x = self.con.x
        self.miracle_name.rect.y = self.con.y

    def get_miracles(self, miracles):
        with open("data/miracles/cantrips.json", "r") as c:
            cantrips = json.load(c)
            for m in miracles['cantrips']:
                self.miracles['cantrips'][cantrips[m]['name']] = cantrips[m]
        with open("data/miracles/lv1.json", "r") as m1:
            miracles1 = json.load(m1)
            for m1 in miracles['lv1']:
                self.miracles['lv1'][miracles1[m1]['name']] = miracles1[m1]
    
    def update(self):
        if self.active == False:
            return
        if self.state == 0:
            for l_btn in self.level_buttons:
                l_btn.update()
        elif self.state == 1:
            for m_btn in self.miracle_buttons:
                m_btn.update()

    def check_click(self, pos=None):
        if self.active == False:
            return
        pos = pos if pos else pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.state == 0:
                for lv_btn in self.level_buttons:
                    val = lv_btn.check_click(pos)
                    if val:
                        self.state = 1
                        self.sub_state = val.replace(" ", "")
                        self.change_title(val)
                        self.get_miracle_buttons(self.con)
                        break
            elif self.state == 1:
                if self.go_back_img_rect.collidepoint(pos):
                    self.state = 0
                for m_btn in self.miracle_buttons:
                    val = m_btn.check_click(pos)
                    if val:
                        self.change_title('')
                        self.name = val
                        self.get_info_text()
                        self.state = 2
                        break
            else:
                if self.go_back_img_rect.collidepoint(pos):
                    self.state = 0
        else:
            self.active = False

    def change_title(self, text):
        self.title = PlainText(text)
        self.title.rect.centerx = self.rect.centerx
        self.title.rect.y = self.rect.y + 40
        self.go_back_img_rect = self.go_back_img.get_rect(centery = self.title.rect.centery, right = self.title.rect.left - 4)

    def blitme(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
            screen.blit(self.title.text, self.title.rect)
            if self.state == 0:
                for l_btn in self.level_buttons:
                    l_btn.blitme(screen)
            elif self.state == 1:
                screen.blit(self.go_back_img, self.go_back_img_rect)
                for m_btn in self.miracle_buttons:
                    m_btn.blitme(screen)
            else:
                screen.blit(self.go_back_img, self.go_back_img_rect)
                screen.blit(self.miracle_name.text, self.miracle_name.rect)