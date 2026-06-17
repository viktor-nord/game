import pygame

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
        holder = Image('assets/ui_sprites/Sprites/Content/5 Holders/7.png', parent=t.rect_relative.move(48,0))
        q = Text("Q", size=14, color=(0,0,0), font_family='freesansbold.ttf', parent=holder.rect, is_bold=False)
        self.end_btn.surf.blit(t.text, t.rect_relative)
        self.end_btn.surf.blit(holder.image, holder.rect)
        self.end_btn.surf.blit(q.text, q.rect)

    def render_action_pannel(self, char):
        # Render BG
        url = 'assets/ui_sprites/Sprites/Content/'
        start = Image(url + '5 Holders/26.png')
        middle = Image(url + '5 Holders/27.png')
        end = Image(url + '5 Holders/28.png')
        margin = 4
        width = 98 if char.steps_amount < 11 else 108
        self.action_pannel = pygame.Surface((start.width + width + end.width, start.height), pygame.SRCALPHA).convert_alpha()
        self.action_pannel_rect = self.action_pannel.get_rect(centerx = self.settings.screen_width / 2, bottom = self.settings.screen_height)
        self.action_pannel.blit(start.image, (0,0))
        x = start.width
        self.action_pannel.blit(middle.image, (x, 0))
        while x < width:
            x += middle.width
            self.action_pannel.blit(middle.image, (x, 0))
        self.action_pannel.blit(end.image, end.image.get_rect(right = self.action_pannel_rect.width))
        # Render Content
        dic = {'box': char.actions_amount, 'triangle': char.bonus_action_amount, 'circle': char.steps_amount}
        x = start.width
        centery = self.action_pannel_rect.height / 2
        for key, val in dic.items():
            color = 'green' if val > 0 else 'red'
            img = pygame.image.load(url + f'2 Icons/{color}-{key}.png').convert_alpha()
            text = Text(str(val), color=(0,0,0))
            self.action_pannel.blit(img, img.get_rect(x = x, centery = centery))
            x += img.get_width() + margin
            self.action_pannel.blit(text, text.get_rect(x = x, centery = centery))
            x += text.get_width() + margin

    def render_characters_display(self):
        index = 0
        self.cards = []
        for key, val in self.characters.items():
            self.cards.append(CharacterCard(key, index, (val.hp, val.max_hp), index == self.active_index))
            index += 1
        card_width = self.cards[0].rect.width
        self.characters_display = pygame.Surface((len(self.cards) * card_width, card_width), pygame.SRCALPHA).convert_alpha()
        self.characters_display_rect = self.characters_display.get_rect(centerx = self.settings.screen_width / 2, y = 2)
        for i, card in enumerate(self.cards):
            self.characters_display.blit(card.image, (card_width * i, 0))

    def render_current_character(self):
        self.character_display = pygame.Surface((300,64), pygame.SRCALPHA).convert_alpha()
        self.character_display_rect = self.character_display.get_rect(left = 10, bottom = self.settings.screen_height - 10)
        name_font = pygame.font.Font('freesansbold.ttf', 22)
        data_font = pygame.font.Font('freesansbold.ttf', 18)
        name_text = self.characters[self.current_character_id].id.capitalize()
        name = name_font.render(name_text, True, (0,0,0))
        data_text = data_font.render('Lv 7 Betuttad Monk', True, (0,0,0))
        for c in self.cards:
            if c.id == self.current_character_id:
                img = c.portret
        self.character_display_img_rect = img.get_rect()
        self.character_display.blit(img, self.character_display_img_rect)
        self.character_display.blit(name, name.get_rect(
            x = self.character_display_img_rect.right + 8, 
            top = self.character_display_img_rect.top + 14
        ))
        self.character_display.blit(data_text, data_text.get_rect(
            x = self.character_display_img_rect.right + 8, 
            top = self.character_display_img_rect.top + 36
        ))

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
        self.max_hp = hp[1]
        self.hp = hp[0]
        self.index = index
        self.is_active = is_active
        bg_img = pygame.image.load('assets/ui_sprites/Sprites/Content/5 Holders/20250420manaSoul9SlicesB-Sheet.png').convert_alpha()
        self.bg = pygame.transform.scale(bg_img, (76,76))
        active_bg_img = pygame.image.load('assets/ui_sprites/Sprites/Content/5 Holders/20250420manaSoul9SlicesC-Sheet.png').convert_alpha()
        self.active_bg = pygame.transform.scale(active_bg_img, (76,76))
        self.image = pygame.Surface((76,76), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        if is_active:
            self.image.blit(self.active_bg, (0,0))
        else:
            self.image.blit(self.bg, (0,0))
        portret = pygame.image.load('assets/ui_sprites/character/' + images[index]).convert_alpha()
        self.portret = pygame.transform.scale(portret, (64,64))
        self.portret_rect = self.portret.get_rect(center = self.rect.center)
        self.image.blit(self.portret, self.portret_rect)
        font = pygame.font.Font('freesansbold.ttf', 12)
        hp_text = font.render(f"{self.hp}/{self.max_hp}", True, (255,255,255))
        self.text_shadow = pygame.Surface((hp_text.get_width() + 2, hp_text.get_height() + 2)).convert()
        self.text_shadow.fill(pygame.Color(0,0,0,100))
        text_rect = self.text_shadow.get_rect(center = (self.rect.width / 2, self.rect.height - 8))
        self.image.blit(self.text_shadow, text_rect)
        self.image.blit(hp_text, hp_text.get_rect(center = text_rect.center))

    def change_state(self):
        if self.is_active:
            self.image.blit(self.bg, (0,0))
            self.image.blit(self.portret, self.portret_rect)
            self.is_active = False
        else:
            self.image.blit(self.active_bg, (0,0))
            self.image.blit(self.portret, self.portret_rect)
            self.is_active = True
