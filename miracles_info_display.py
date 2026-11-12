import pygame
import json

from image import Image, add_shadow
from settings import Settings
from font import PlainText
from button import TextButton
# from utils import get_shadow_surf

class MiraclesInfoDisplay:
    def __init__(self, miracles, right_side=True):
        self.settings = Settings()
        self.right_side = right_side
        self.selected_miracle = ''
        self.states = ['level', 'select', 'data']
        self.state = 0
        self.level = 'lv0'
        self.name = 'Miracles'
        self.active = False
        self.miracles = {
            'lv0': {},
            'lv1': {},
            'lv2': {},
            'lv3': {},
            'lv4': {},
            'lv5': {},
        }
        sprite_url = 'assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Plain/8 Shop/1.png'
        y = self.settings.screen_width/2 if right_side else 0
        img_parent = pygame.Rect((y, 0), (self.settings.screen_height, self.settings.screen_width/2))
        self.image = Image(sprite_url, parent=img_parent, shadow_dir="left")
        self.rect = self.image.rect

        container = pygame.Rect((50, 64), (256, 20))
        self.get_miracles(miracles)
        self.con = container.move(self.rect.topleft).move(36, 20)
        self.title = PlainText("Miracles")
        self.title.rect.centerx = self.rect.centerx
        self.title.rect.y = self.rect.y + 64
        self.level_buttons = self.get_lv_buttons(self.con)
        self.miracle_buttons = self.get_miracle_buttons(self.con)
        self.tooltip = MiracleTooltip(self.miracles['lv0']['Holy Mockery'])

    def get_lv_buttons(self, container):
        labels = [
            {'text': 'lv 0', 'value': 'lv0', 'index': 0},
            {'text': 'lv 1', 'value': 'lv1', 'index': 1},
            {'text': 'lv 2', 'value': 'lv2', 'index': 2},
            {'text': 'lv 3', 'value': 'lv3', 'index': 3},
            {'text': 'lv 4', 'value': 'lv4', 'index': 4},
            {'text': 'lv 5', 'value': 'lv5', 'index': 5},
        ]
        arr = []
        for l in labels:
            arr.append(TextButton(
                l['text'], 
                container.move(42 * l['index'], 0), 
                value=l['value'], 
                border=True))
        return arr
    
    def get_miracle_buttons(self, container):
        arr = []
        i = 0
        for key, val in self.miracles[self.level].items():
            arr.append(TextButton(
                key, 
                container.move(0, 24 + 18 * i), 
                value=val, 
                tooltip=MiracleTooltip(val), 
                right_icon=True, 
                border=False
            ))
            i += 1
        return arr

    def get_info_text(self):
        self.miracle_name = PlainText(self.name)
        self.miracle_name.rect.x = self.con.x
        self.miracle_name.rect.y = self.con.y

    def get_miracles(self, miracles):
        with open("data/miracles/lv0.json", "r") as c:
            lv0 = json.load(c)
            for val in miracles['lv0']:
                self.miracles['lv0'][lv0[val]['name']] = lv0[val]
        with open("data/miracles/lv1.json", "r") as m1:
            miracles1 = json.load(m1)
            for m1 in miracles['lv1']:
                self.miracles['lv1'][miracles1[m1]['name']] = miracles1[m1]

    def find_miracle_level(self, miracle):
        for key, val in self.miracles.items():
            for name in val.keys():
                if name == miracle:
                    return key

    def update(self):
        if self.active == False:
            return
        [x.update() for x in self.level_buttons]
        [x.update() for x in self.miracle_buttons]

    def check_click(self, pos=None):
        if self.active == False:
            return
        pos = pos if pos else pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.check_lv_button(pos)
            self.check_miracle_button(pos)
        else:
            self.active = False

    def check_lv_button(self, pos):
        for lv_btn in self.level_buttons:
            val = lv_btn.check_click(pos)
            if val:
                self.level = val
                self.change_title(val)
                self.miracle_buttons = self.get_miracle_buttons(self.con)
                break

    def check_miracle_button(self, pos):
        for m_btn in self.miracle_buttons:
            val = m_btn.check_click(pos)
            if val:
                self.selected_miracle = val['name']

    def change_title(self, text):
        self.title = PlainText(text)
        self.title.rect.centerx = self.rect.centerx
        self.title.rect.y = self.rect.y + 64

    def blitme(self, screen):
        if self.active == False:
            return
        screen.blit(self.image.surf, self.rect)
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
        img_url = 'assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Plain/5 Mini Map/1.png'
        img = Image(img_url, shadow_dir="right")
        self.surf = add_shadow(img.image)
        url = "assets/ui_sprites/node_2D/icon_"
        if self.damage:
            damage = f"{self.damage['amount']}d{self.damage['dice']}" 
        else:
            damage = "None"
        blueprint = [
            {'text': damage, 'img': Image(f'{url}dice.png')},
            {'text': f"{self.range}", 'img': Image(f'{url}target_2.png')},
            {'text': f"{self.effect[0]}", 'img': Image(f'{url}particle.png')},
            {'text': f"{self.duration}", 'img': Image(f'{url}time.png')},
        ]
        self.render_img(blueprint)

    def set_value(self, value):
        self.name = value['name']
        self.desc = value['desc']
        self.range = value['range']
        self.duration = value['duration']
        self.concentration = value['concentration']
        self.casting_time = value['casting_time']
        self.level = value['level']
        # self.school = value['school']
        self.damage = value['damage']
        # self.dc = value['dc']
        self.effect = value['effect'] if len(value['effect']) > 0 else "none"

    def render_img(self, blueprint):
        x, y = 58, 94
        r = pygame.Rect((0,74),(self.surf.get_width(), 16))
        text = PlainText(self.name, parent=r)
        self.surf.blit(text.text, text.rect)
        # x, y = 50, 68
        for val in blueprint:
            t = PlainText(val['text'])
            self.surf.blit(val['img'].surf, (x, y))
            self.surf.blit(t.text, (x + 20, y))
            y += 20

    def blitme(self, screen, pos=None):
        p = pos if pos else pygame.mouse.get_pos()
        screen.blit(self.surf, p)
