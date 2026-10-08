import pygame
from settings import Settings
from font import AnimatedText, Text
from image import get_title_holder

dialog_texts = {
    "mike": [
        {
            "1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9": None
        },
        {
            "my name is jon. this is a long test. that i hopfully going to skip to the next line. i will just keep typing shit untill the lenght is long enought.": None
        },
        {
            "godbye": None
        }
    ],
    "bob": [
        {"mysnamesissjonssthississaslongstestw thatsishopfully mysnamesissjon.sthississaslongstest. thatsishopfully": None}
    ],
    "jim": [{"Def": None}],
    "else": [{"don't talk to me": None}],
    "ulf": [
        {
            'What do you want?': None
        },
        {
            "Experience the city": {
                "then you should go to the tavern": None
            },
            "Find a home": {
                'What type of home?': {
                    "A small one": None,
                    "A big one": None
                }
            },
            "Nothing": None
        },
        {
            "I wish you good luck": None
        },
    ],
}


class Dialog:
    def __init__(self, npc, player, animated=True):
        self.settings = Settings()
        self.done = False
        self.text_array = dialog_texts['ulf']
        # self.text_array = dialog_texts[npc.id] if npc else dialog_texts["else"]
        self.counter = 0
        raw_text = next(iter(self.text_array[self.counter]))
        self.current_dialog = self.text_array[self.counter][raw_text]
        self.animated = animated
        src = 'assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Folding & Cutout/7 Dialogue Box/'
        self.image = pygame.image.load(src + '1_small.png').convert_alpha()
        self.last_image = pygame.image.load(
            src + '2_small.png').convert_alpha()
        self.book_img = pygame.image.load(
            'assets/ui_sprites/Sprites/Content/2 Icons/23.png').convert_alpha()
        self.rect = self.image.get_rect(
            centerx=self.settings.screen_width / 2, bottom=self.settings.screen_height)
        self.text_box = pygame.Rect(
            (self.rect.x + 32, self.rect.y + 50), (self.rect.width - 32*2, self.rect.height - 50*2))
        self.text = AnimatedText(raw_text, self.text_box)
        self.player_is_speeking = False
        self.options = []
        if npc:
            self.npc = self.get_char_img(npc, False)
            self.title = self.render_title(npc)
        if player:
            self.player = self.get_char_img(player, True)

    def get_char_img(self, char, is_player):
        img = char.character_sprite.display_image
        if is_player:
            center = self.rect.move(64, -16).topleft 
        else:
            center = self.rect.move(-64, -16).topright
        rect = img.get_rect(center=center)
        return {'img': img, 'rect': rect}

    def render_title(self, npc):
        holder = get_title_holder(98)
        surf, rect = holder['surf'], holder['rect']
        rect.centerx = self.settings.screen_width // 2
        rect.bottom = self.settings.screen_height - 8
        name = Text(npc.id, rect, color=(223, 240, 216))
        surf.blit(name.text, name.relative_rect)
        return {'surf': surf, 'rect': rect}

    def create_options(self, options):
        val = []
        text_height = 20
        t = self.text_box
        for i, option in enumerate(options.keys()):
            r = pygame.Rect((t.x + 32, t.y + text_height*i), (t.width, 20))
            text = Text(option, r)
            val.append({'text': text.text, 'rect': r, 'val': option})
        return val

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        for op in self.options:
            if op['rect'].collidepoint(pos):
                return op['val']
        return None

    def check_current_is_none(self):
        if self.current_dialog == None:
            return True
        if next(iter(self.current_dialog)) == None:
            return True
        return False

    def check_to_render_text(self):
        if self.text.animation_done or len(self.options):
            return False
        if self.player_is_speeking == False:
            return True
        return False

    def next_line(self):
        self.counter += 1
        self.current_dialog = self.text_array[self.counter]
        t = next(iter(self.current_dialog))
        self.text = AnimatedText(t, self.text_box)

    def handle_options(self):
        click_val = self.handle_click()
        if click_val == None:
            return
        self.player_is_speeking = False
        self.options = []
        if self.current_dialog[click_val] == None:
            self.next_line()
        else:
            t = next(iter(self.current_dialog[click_val]))
            self.current_dialog = self.current_dialog[click_val][t]
            self.text = AnimatedText(t, self.text_box)

    def next(self):
        # if dialog is done but there is still text being typed
        if self.check_to_render_text():
            self.text.render_all_text()
            return
        if self.counter + 1 >= len(self.text_array):
            self.done = True
            return
        if self.check_current_is_none():
            self.next_line()
        if len(self.current_dialog) > 1:
            self.options = self.create_options(self.current_dialog)
            if self.player_is_speeking:
                self.handle_options()
                return
            self.player_is_speeking = True
        else:
            self.player_is_speeking = False

    def blitme(self, screen):
        if self.npc:
            screen.blit(self.npc['img'], self.npc['rect'])
        if self.player:
            screen.blit(self.player['img'], self.player['rect'])
        if self.counter < len(self.text_array):
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.last_image, self.rect)
        if self.player_is_speeking:
            for o in self.options:
                screen.blit(o['text'], o['rect'])
        else:
            self.text.blitme(screen)
        if self.npc:
            screen.blit(self.title['surf'], self.title['rect'])
