import pygame

from settings import Settings

class BattleUI():
    def __init__(self, characters):
        self.characters = characters
        self.settings = Settings()
        self.active_index = 0
        self.cards = []
        self.current_character_id = 'player'
        self.render_characters_display()
        self.render_current_character()
        action = 1
        bonus_action = 0
        speed = 10
        self.render_action_pannel(action, bonus_action, speed)
        # self.action_pannel = pygame.Surface(())

    def get_scaled_img(self, path, scale=2):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))

    def render_action_pannel(self, action, bonus, speed):
        url = 'assets/ui_sprites/Sprites/Content/'
        start = self.get_scaled_img(url + '5 Holders/26.png')
        middle = self.get_scaled_img(url + '5 Holders/27.png')
        end = self.get_scaled_img(url + '5 Holders/28.png')
        font = pygame.font.Font('freesansbold.ttf', 18)
        action_url = '2 Icons/green-box.png' if action > 0 else '2 Icons/red-box.png'
        action_img = pygame.image.load(url + action_url).convert_alpha()
        bonus_url = '2 Icons/green-triangle.png' if bonus > 0 else '2 Icons/red-triangle.png'
        bonus_img = pygame.image.load(url + bonus_url).convert_alpha()
        speed_url = '2 Icons/green-circle.png' if speed > 0 else '2 Icons/red-circle.png'
        speed_img = pygame.image.load(url + speed_url).convert_alpha()
        action_text = font.render(str(action), True, (0,0,0))
        bonus_action_text = font.render(str(bonus), True, (0,0,0))
        speed_text = font.render(str(speed), True, (0,0,0))
        margin = 4
        width = action_img.get_width() * 3 + margin * 5 + action_text.get_width() + bonus_action_text.get_width() + speed_text.get_width()
        self.action_pannel = pygame.Surface((start.get_width() + width + end.get_width(), start.get_height()), pygame.SRCALPHA).convert_alpha()
        self.action_pannel_rect = self.action_pannel.get_rect(centerx = self.settings.screen_width / 2, bottom = self.settings.screen_height)
        self.action_pannel.blit(start, (0,0))
        while_x = start.get_width()
        while while_x < width:
            self.action_pannel.blit(middle, (while_x,0))
            while_x += middle.get_width()
        self.action_pannel.blit(middle, middle.get_rect(right = self.action_pannel_rect.width - end.get_width()))
        self.action_pannel.blit(end, end.get_rect(right = self.action_pannel_rect.width))
        x = start.get_width()
        centery = self.action_pannel_rect.height / 2
        self.action_pannel.blit(action_img, action_img.get_rect(x = x, centery = centery))
        x += action_img.get_width() + margin
        self.action_pannel.blit(action_text, action_text.get_rect(x = x, centery = centery))
        x += action_text.get_width() + margin
        self.action_pannel.blit(bonus_img, bonus_img.get_rect(x = x, centery = centery))
        x += bonus_img.get_width() + margin
        self.action_pannel.blit(bonus_action_text, bonus_action_text.get_rect(x = x, centery = centery))
        x += bonus_action_text.get_width() + margin
        self.action_pannel.blit(speed_img, speed_img.get_rect(x = x, centery = centery))
        x += speed_img.get_width() + margin
        self.action_pannel.blit(speed_text, speed_text.get_rect(x = x, centery = centery))

    def render_characters_display(self):
        index = 0
        self.cards = []
        for key in self.characters.keys():
            self.cards.append(CharacterCard(key, index, index == self.active_index))
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
        self.character_display.blit(name, name.get_rect(x = self.character_display_img_rect.right + 8, top = self.character_display_img_rect.top + 14))
        self.character_display.blit(data_text, data_text.get_rect(x = self.character_display_img_rect.right + 8, top = self.character_display_img_rect.top + 36))

    def update(self):
        self.active_index += 1
        self.render_characters_display()

    def blitme(self, screen):
        screen.blit(self.characters_display, self.characters_display_rect)
        screen.blit(self.character_display, self.character_display_rect)
        screen.blit(self.action_pannel, self.action_pannel_rect)

    def handle_action(self):
        pass

    def handle_click(self):
        pass

class CharacterCard:
    def __init__(self, id, index, is_active=False):
        images = ["Frame 19.png", "Frame 20.png", "Frame 21.png", "Frame 22.png", "Frame 23.png", "Frame 24.png", "Frame 25.png", "Frame 26.png"]
        self.id = id
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

    def change_state(self):
        if self.is_active:
            self.image.blit(self.bg, (0,0))
            self.image.blit(self.portret, self.portret_rect)
            self.is_active = False
        else:
            self.image.blit(self.active_bg, (0,0))
            self.image.blit(self.portret, self.portret_rect)
            self.is_active = True
