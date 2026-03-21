import pygame
import json

from settings import Settings
from font import PlainText
from button import TextButton
from utils import get_shadow_surf

class MiraclesInfoDisplay:
    def __init__(self, miracles, right_side=True):
        self.settings = Settings()
        self.right_side = right_side
        self.selected_miracle = ''
        self.sprite = pygame.image.load('assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Plain/8 Shop/1.png').convert_alpha()
        self.shadow = get_shadow_surf(self.sprite)
        self.image = pygame.Surface((self.sprite.get_width(), self.sprite.get_height()), pygame.SRCALPHA).convert_alpha()
        rect_right = self.settings.screen_width if self.right_side else self.sprite.get_width()
        self.rect = self.image.get_rect(centery = self.settings.screen_height / 2, right = rect_right)
        self.image.blit(self.sprite, (0,0))
        self.container = pygame.Rect((50, 64), (256, 20))
        self.active = False
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
        self.level = 'cantrips'
        self.name = 'Miracles'
        self.con = self.container.move(self.rect.topleft).move(36, 20)
        self.title = PlainText("Miracles")
        self.title.rect.centerx = self.rect.centerx
        self.title.rect.y = self.rect.y + 64
        self.level_buttons = self.get_lv_buttons(self.con)
        self.miracle_buttons = self.get_miracle_buttons(self.con)
        self.tooltip = MiracleTooltip(self.miracles['cantrips']['holy tomfoolery'])

    def get_lv_buttons(self, container):
        labels = [
            {'text': 'lv 0', 'value': 'cantrips', 'index': 0},
            {'text': 'lv 1', 'value': 'lv1', 'index': 1},
            {'text': 'lv 2', 'value': 'lv2', 'index': 2},
            {'text': 'lv 3', 'value': 'lv3', 'index': 3},
            {'text': 'lv 4', 'value': 'lv4', 'index': 4},
            {'text': 'lv 5', 'value': 'lv5', 'index': 5},
        ]
        arr = []
        for l in labels:
            arr.append(TextButton(l['text'], container.move(42 * l['index'], 0), value=l['value'], border=True))
        return arr
    
    def get_miracle_buttons(self, container):
        arr = []
        i = 0
        for key, val in self.miracles[self.level].items():
            arr.append(TextButton(key, container.move(0, 24 + 18 * i), value=val, tooltip=MiracleTooltip(val), right_icon=True, border=False))
            i += 1
        return arr

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
        for l_btn in self.level_buttons:
            l_btn.update()
        for m_btn in self.miracle_buttons:
            m_btn.update()

    def check_click(self, pos=None):
        if self.active == False:
            return
        pos = pos if pos else pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            for lv_btn in self.level_buttons:
                val = lv_btn.check_click(pos)
                if val:
                    self.level = val
                    self.change_title(val)
                    self.miracle_buttons = self.get_miracle_buttons(self.con)
                    break
            for m_btn in self.miracle_buttons:
                val = m_btn.check_click(pos)
                if val:
                    self.selected_miracle = val['name']
        else:
            self.active = False

    def change_title(self, text):
        self.title = PlainText(text)
        self.title.rect.centerx = self.rect.centerx
        self.title.rect.y = self.rect.y + 64

    def blitme(self, screen):
        if self.active:
            screen.blit(self.shadow, self.rect)
            screen.blit(self.image, self.rect)
            screen.blit(self.title.text, self.title.rect)
            for l_btn in self.level_buttons:
                l_btn.blitme(screen)
            for m_btn in self.miracle_buttons:
                m_btn.blitme(screen)
            for b2 in self.miracle_buttons:
                if b2.is_hover and b2.tooltip:
                    x, y = pygame.mouse.get_pos() 
                    b2.tooltip.blitme(screen, (x - 20, y - 20))
            
class MiracleTooltip:
    def __init__(self, value):
        self.settings = Settings()
        self.active = False
        self.set_value(value)
        img = pygame.image.load('assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Plain/5 Mini Map/1.png').convert_alpha()
        self.surf = pygame.Surface((img.get_width(), img.get_height()), pygame.SRCALPHA).convert_alpha()
        self.surf.blit(img, (0,0))
        blueprint = [
            {'text': f"{self.damage_level['1']}d{self.damage_die}", 'img': pygame.image.load('assets/ui_sprites/node_2D/icon_dice.png').convert_alpha()},
            {'text': self.range, 'img': pygame.image.load('assets/ui_sprites/node_2D/icon_target_2.png').convert_alpha()},
            {'text': self.effect, 'img': pygame.image.load('assets/ui_sprites/node_2D/icon_particle.png').convert_alpha()},
            {'text': self.duration, 'img': pygame.image.load('assets/ui_sprites/node_2D/icon_time.png').convert_alpha()},
        ]
        self.render_img(blueprint)
        self.shadow = get_shadow_surf(img)

    def set_value(self, value):
        self.name = value['name']
        self.index = value['index']
        self.desc = value['desc']
        self.range = value['range']
        self.is_ritual = value['ritual']
        self.duration = value['duration']
        self.concentration = value['concentration']
        self.casting_time = value['casting_time']
        self.level = value['level']
        self.school = value['school']
        # change this shit
        try:
            self.damage_type = value['damage']['damage_type']
            self.damage_die = value['damage']['die']
            self.damage_level = value['damage']['level']
            self.dc = value['dc'] # 'dc': {'dc_type': 'dex', 'dc_success': 'none'
            self.effect = value['effect'][0]['type']
        except KeyError:
            self.damage_type = 'None'
            self.damage_die = '0'
            self.damage_level = {"1": 0, "5": 0, "11": 0, "17": 0}
            self.dc = 'None'
            self.effect = 'None'

    def render_img(self, blueprint):
        self.surf.blit(PlainText(self.name).text, (50, 52))
        x, y = 50, 68
        for val in blueprint:
            t = PlainText(val['text'])
            self.surf.blit(val['img'], (x, y))
            self.surf.blit(t.text, (x + 20, y))
            y += 20

    def blitme(self, screen, pos=None):
        p = pos if pos else pygame.mouse.get_pos()
        screen.blit(self.shadow, p)
        screen.blit(self.surf, p)
