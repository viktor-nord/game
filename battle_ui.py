from matplotlib.pyplot import draw
import pygame
from container import Container
from image import Image
from settings import Settings
from font import PlainText, Text

class BattleUI:
    def __init__(self, battle_class, characters, current_id='player'):
        self.battle_class = battle_class
        self.characters = characters
        self.settings = Settings()
        self.current_character_id = current_id
        self.active_index = list(self.characters.keys()).index(current_id)
        self.cards = []
        self.render_characters_display()
        self.render_current_character()
        self.render_action_pannel(self.characters[self.current_character_id])
        self.render_end_turn_button()

    def get_scaled_img(self, path, scale=2):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))

    def render_end_turn_button(self):
        url = 'assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Folding & Cutout/4 Notification/2.png'
        container = pygame.Rect((self.settings.screen_width / 2, 0),(1,1))
        self.end_btn = Image(url, scale=0.5, parent=container)
        self.end_btn.rect.bottom = self.action_pannel_rect.top
        t = PlainText('End Turn ', parent=self.end_btn.rect)
        t.rect_relative = t.rect_relative.move(0,5)
        holder = Image(
            'assets/ui_sprites/Sprites/Content/5 Holders/7.png', 
            parent=t.rect_relative.move(48,0)
        )
        q = Text(
            "Q", 
            size=14, 
            color=(0,0,0), 
            font_family='freesansbold.ttf', 
            parent=holder.rect, 
            is_bold=False
        )
        self.end_btn.surf.blit(t.text, t.rect_relative)
        self.end_btn.surf.blit(holder.image, holder.rect)
        self.end_btn.surf.blit(q.text, q.rect)

    def render_action_pannel(self, char):
        url = 'assets/ui_sprites/Sprites/Content/'
        self.render_action_pannel_bg(url, char.steps_amount)
        self.render_action_pannel_content(url, char)

    def render_action_pannel_bg(self, url, steps):
        start = Image(url + '5 Holders/26.png')
        middle = Image(url + '5 Holders/27.png')
        end = Image(url + '5 Holders/28.png')
        width = 98 if steps < 11 else 108
        wh = (start.width + width + end.width, start.height)
        self.action_pannel = pygame.Surface(wh, pygame.SRCALPHA).convert_alpha()
        self.action_pannel_rect = self.action_pannel.get_rect(
            centerx = self.settings.screen_width / 2, 
            bottom = self.settings.screen_height
        )
        self.action_pannel.blit(start.image, (0,0))
        x = start.width
        self.action_pannel.blit(middle.image, (x, 0))
        while x < width:
            x += middle.width
            self.action_pannel.blit(middle.image, (x, 0))
        self.action_pannel.blit(
            end.image, end.image.get_rect(right = self.action_pannel_rect.width)
        )

    def render_action_pannel_content(self, url, char):
        dic = {'box': char.actions_amount, 'triangle': char.bonus_action_amount, 'circle': char.steps_amount}
        margin, x, centery = 4, 36, self.action_pannel_rect.height / 2
        for key, val in dic.items():
            color = 'green' if val > 0 else 'red'
            img = pygame.image.load(url + f'2 Icons/{color}-{key}.png').convert_alpha()
            self.action_pannel.blit(img, img.get_rect(x = x, centery = centery))
            x += img.get_width() + margin
            text = Text(str(val), color=(0,0,0))
            self.action_pannel.blit(text.text, text.text.get_rect(x = x, centery = centery))
            x += text.text.get_width() + margin

    def render_characters_display(self):
        self.cards = []
        for i, (key, val) in enumerate(self.characters.items()):
            self.cards.append(CharacterCard(key, i, (val.hp, val.max_hp), i == self.active_index))
        card_width = self.cards[0].rect.width
        self.characters_display = pygame.Surface((len(self.cards) * card_width, card_width), pygame.SRCALPHA).convert_alpha()
        self.characters_display_rect = self.characters_display.get_rect(centerx = self.settings.screen_width / 2, y = 2)
        for i, card in enumerate(self.cards):
            self.characters_display.blit(card.image, (card_width * i, 0))

    def render_current_character(self):
        self.character_display = pygame.Surface((300, 64), pygame.SRCALPHA).convert_alpha()
        self.character_display_rect = self.character_display.get_rect(left = 10, bottom = self.settings.screen_height - 10)
        img = next(c.portret for c in self.cards if c.id == self.current_character_id)
        r = img.rect
        name_pos = (r.right + 8, r.top + 14)
        data_pos = (r.right + 8, r.top + 36)
        name_text = self.characters[self.current_character_id].id.capitalize()
        name = Text(name_text, font_family='freesansbold.ttf', color=(71,128,178), is_bold=False, pos=name_pos)
        data = Text('Lv 7 Betuttad Monk', font_family='freesansbold.ttf', color=(71,128,178), is_bold=False, pos=data_pos, size=22)
        self.character_display.blit(img.image, r)
        self.character_display.blit(name.text, name.rect)
        self.character_display.blit(data.text, data.rect)

    def update(self):
        self.active_index += 1
        self.render_characters_display()

    def blitme(self, screen):
        screen.blit(self.characters_display, self.characters_display_rect)
        screen.blit(self.character_display, self.character_display_rect)
        screen.blit(self.action_pannel, self.action_pannel_rect)
        screen.blit(self.end_btn.surf, self.end_btn.rect)

    def handle_action(self):
        pass

    def handle_click(self, pos):
        if self.end_btn.rect.collidepoint(pos):
            self.battle_class.end_turn()

class CharacterCard:
    def __init__(self, id, index, hp, is_active=False):
        images = ["Frame 19.png", "Frame 20.png", "Frame 21.png", "Frame 22.png", "Frame 23.png", "Frame 24.png", "Frame 25.png", "Frame 26.png"]
        self.id = id
        self.is_active = is_active
        self.image = pygame.Surface((76,76), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        url = 'assets/ui_sprites/Sprites/Content/5 Holders/'
        self.bg = Image(f"{url}20250420manaSoul9SlicesB-Sheet.png", size=76)
        self.active_bg = Image(f"{url}20250420manaSoul9SlicesC-Sheet.png", size=76)
        if is_active:
            self.image.blit(self.active_bg.image, (0,0))
        else:
            self.image.blit(self.bg.image, (0,0))
        self.portret = Image('assets/ui_sprites/character/' + images[index], size=64, parent=self.bg.rect)
        self.image.blit(self.portret.image, self.portret.rect)
        hp = Text(f"{hp[0]}/{hp[1]}", size=12, color=(255,255,255), font_family='freesansbold.ttf')
        self.text_shadow = pygame.Surface((hp.rect.width + 2, hp.rect.height + 2)).convert()
        self.text_shadow.fill(pygame.Color(0,0,0,50))
        text_rect = self.text_shadow.get_rect(centerx = self.rect.width / 2, bottom = self.rect.height)
        self.image.blit(self.text_shadow, text_rect)
        self.image.blit(hp.text, hp.text.get_rect(center = text_rect.center))

    def change_state(self):
        if self.is_active:
            self.image.blit(self.bg.image, (0,0))
            self.image.blit(self.portret.image, self.portret.rect)
            self.is_active = False
        else:
            self.image.blit(self.active_bg.image, (0,0))
            self.image.blit(self.portret.image, self.portret.rect)
            self.is_active = True
