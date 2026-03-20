import pygame

from settings import Settings
from font import PlainText

class BattleUI:
    def __init__(self, battle_class, characters, current_id='player'):
        self.battle_class = battle_class
        self.characters = characters
        self.settings = Settings()
        self.current_character_id = current_id
        self.get_current_index(current_id)
        self.cards = []
        self.render_characters_display()
        self.render_current_character()
        self.render_action_pannel(self.characters[self.current_character_id])
        self.render_end_turn_button()

    def get_current_index(self, id):
        index = 0
        self.active_index = 0
        for key, val in self.characters.items():
            if key == id:
                self.active_index = index
                return
            else:
                index += 1

    def get_scaled_img(self, path, scale=2):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))

    def render_end_turn_button(self):
        img = self.get_scaled_img('assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Folding & Cutout/4 Notification/2.png', 0.5)
        holder = self.get_scaled_img('assets/ui_sprites/Sprites/Content/5 Holders/7.png', 1)
        self.end_turn_button = pygame.Surface((img.get_width(), img.get_height()), pygame.SRCALPHA).convert_alpha()
        self.end_turn_button_rect = self.end_turn_button.get_rect(centerx = self.settings.screen_width / 2, bottom = self.action_pannel_rect.top)
        self.end_turn_button.blit(img, (0,0))
        t = PlainText('End Turn ')
        font = pygame.font.Font('freesansbold.ttf', 14)
        q = font.render('Q', True, (0,0,0))
        text_rect = t.text.get_rect(center = (self.end_turn_button_rect.width / 2, self.end_turn_button_rect.height / 1.6))
        self.end_turn_button.blit(t.text, text_rect)
        holder_rect = holder.get_rect(centery = text_rect.centery, left = text_rect.right)
        self.end_turn_button.blit(holder, holder_rect)
        self.end_turn_button.blit(q, q.get_rect(center = holder_rect.center))

    def render_action_pannel(self, char):
        action, bonus, speed = char.actions_amount, char.bonus_action_amount, char.steps_amount
        url = 'assets/ui_sprites/Sprites/Content/'
        start = self.get_scaled_img(url + '5 Holders/26.png')
        middle = self.get_scaled_img(url + '5 Holders/27.png')
        end = self.get_scaled_img(url + '5 Holders/28.png')
        font = pygame.font.Font('freesansbold.ttf', 18)
        dic = {'box': action, 'triangle': bonus, 'circle': speed}
        action_dictionary = {'box': {}, 'triangle': {}, 'circle': {}}
        for key, val in dic.items():
            color = 'green' if val > 0 else 'red'
            action_dictionary[key]['img'] = pygame.image.load(url + f'2 Icons/{color}-{key}.png').convert_alpha()
            action_dictionary[key]['text'] = font.render(str(val), True, (0,0,0))
        margin = 4
        width = 98 if speed < 11 else 108
        # width = action_img.get_width() * 3 + margin * 5 + action_text.get_width() + bonus_action_text.get_width() + speed_text.get_width()
        self.action_pannel = pygame.Surface((start.get_width() + width + end.get_width(), start.get_height()), pygame.SRCALPHA).convert_alpha()
        self.action_pannel_rect = self.action_pannel.get_rect(centerx = self.settings.screen_width / 2, bottom = self.settings.screen_height)
        self.action_pannel.blit(start, (0,0))
        while_x = start.get_width()
        while while_x < width:
            self.action_pannel.blit(middle, (while_x, 0))
            while_x += middle.get_width()
        self.action_pannel.blit(middle, middle.get_rect(right = self.action_pannel_rect.width - end.get_width()))
        self.action_pannel.blit(end, end.get_rect(right = self.action_pannel_rect.width))
        x = start.get_width()
        centery = self.action_pannel_rect.height / 2
        for key, val in action_dictionary.items():
            self.action_pannel.blit(val['img'], val['img'].get_rect(x = x, centery = centery))
            x += val['img'].get_width() + margin
            self.action_pannel.blit(val['text'], val['text'].get_rect(x = x, centery = centery))
            x += val['text'].get_width() + margin

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
        screen.blit(self.end_turn_button, self.end_turn_button_rect)

    def handle_action(self):
        pass

    def handle_click(self, pos):
        if self.end_turn_button_rect.collidepoint(pos):
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
        self.text_shadow.fill((0,0,0))
        self.text_shadow.set_alpha(100)
        text_rect = self.text_shadow.get_rect(center = (self.rect.width / 2, self.rect.height - 8))
        self.image.blit(self.text_shadow, text_rect)
        self.image.blit(hp_text, hp_text.get_rect(center = text_rect.center))
        name = font.render(f"{id}", True, (255,255,255))
        shit = pygame.Surface((name.get_width() + 4, name.get_height() + 4)).convert()
        shit.fill((0,0,0))
        shit.set_alpha(100)
        self.image.blit(shit, shit.get_rect(center = self.rect.center))
        self.image.blit(name, name.get_rect(center = self.rect.center))

    def change_state(self):
        if self.is_active:
            self.image.blit(self.bg, (0,0))
            self.image.blit(self.portret, self.portret_rect)
            self.is_active = False
        else:
            self.image.blit(self.active_bg, (0,0))
            self.image.blit(self.portret, self.portret_rect)
            self.is_active = True
