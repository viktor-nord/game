import pygame
from settings import Settings
from font import AnimatedText, Text
from image import Image

dialog_texts = {
    "mike": [
        "1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9", 
        "my name is jon. this is a long test. that i hopfully going to skip to the next line. i will just keep typing shit untill the lenght is long enought.", 
        "godbye"
    ],
    "bob": ["mysnamesissjonssthississaslongstestw thatsishopfully mysnamesissjon.sthississaslongstest. thatsishopfully"],
    "jim": ["Def"],
    "else": ["don't talk to me"],
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
    "ulf2": [
        [
            'What do you want?'
        ],
        [
            "Experience the city", 
            [
                "then you should go to the tavern"
            ],
            "Find a home",
            [
                'What type of home?',
                [
                    "A small one",
                    "A big one"
                ]
            ],
            "Nothing"
        ],
        [
            "I wish you good luck"
        ]
    ]
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
        self.last_image = pygame.image.load(src + '2_small.png').convert_alpha()
        self.book_img = pygame.image.load('assets/ui_sprites/Sprites/Content/2 Icons/23.png').convert_alpha()
        self.rect = self.image.get_rect(centerx = self.settings.screen_width / 2, bottom = self.settings.screen_height)
        self.text_box = pygame.Rect((self.rect.x + 32, self.rect.y + 50),(self.rect.width - 32*2, self.rect.height - 50*2))
        self.text = AnimatedText(raw_text, self.text_box, has_underline=False)
        # self.text = AnimatedText(self.text_array[self.counter], self.text_box, has_underline=False)
        self.player_is_speeking = False
        self.options = []
        if npc:
            self.npc = self.get_char_img(npc, False)
            self.title = self.render_title(npc)
        if player:
            self.player = self.get_char_img(player, True)

    def get_char_img(self, char, is_player):
        img = char.character_sprite.display_image
        center = self.rect.move(64, -16).topleft if is_player else self.rect.move(-64, -16).topright
        rect = img.get_rect(center=center)
        return {'img': img, 'rect': rect}

    def render_title(self, npc):
        url = 'assets/ui_sprites/Sprites/Content/'
        start = Image(url + '5 Holders/26.png')
        middle = Image(url + '5 Holders/27.png')
        end = Image(url + '5 Holders/28.png')
        width = 98
        # width = 98 if steps < 11 else 108
        wh = (start.width + width + end.width, start.height)
        title = pygame.Surface(wh, pygame.SRCALPHA).convert_alpha()
        rect = title.get_rect(
            centerx = self.settings.screen_width / 2, 
            bottom = self.settings.screen_height - 8
        )
        title.blit(start.image, (0,0))
        x = start.width
        title.blit(middle.image, (x, 0))
        while x < width:
            x += middle.width
            title.blit(middle.image, (x, 0))
        title.blit(
            end.image, end.image.get_rect(right = rect.width)
        )
        name = Text(npc.id, rect, color=(223,240,216))
        title.blit(name.text, name.relative_rect)
        return {'title': title, 'rect': rect}

    def create_options(self, options):
        val = []
        text_height = 20
        for i, option in enumerate(options.keys()):
            r = pygame.Rect((self.text_box.x + 32, self.text_box.y + text_height*i), (self.text_box.width, 20))
            text = Text(option, r)
            val.append({'text': text.text, 'rect': r, 'val': option})
        return val

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        for op in self.options:
            if op['rect'].collidepoint(pos):
                return op['val']
        return None

    def check_if_next_line(self):
        if self.current_dialog == None:
            return True
        if next(iter(self.current_dialog)) == None:
            return True
        return False

    def next(self):
        if self.text.animation_done or len(self.options):
            if self.counter +1 >= len(self.text_array):
                self.done = True
                return
            if self.check_if_next_line():
                self.counter += 1
                self.current_dialog = self.text_array[self.counter]
                t = next(iter(self.current_dialog))
                self.text = AnimatedText(t, self.text_box, has_underline=False)
            if len(self.current_dialog) > 1:
                # self.player_is_speeking = True
                self.options = self.create_options(self.current_dialog)
                if self.player_is_speeking:
                    click_val = self.handle_click()
                    if click_val:
                        if self.current_dialog[click_val] == None:
                            self.counter += 1
                            self.current_dialog = self.text_array[self.counter]
                            t = next(iter(self.current_dialog))
                            self.text = AnimatedText(t, self.text_box, has_underline=False)
                            self.player_is_speeking = False
                            self.options = []
                            return
                        else:
                            t = next(iter(self.current_dialog[click_val]))
                            self.current_dialog = self.current_dialog[click_val][t]
                            self.text = AnimatedText(t, self.text_box, has_underline=False)
                            self.player_is_speeking = False
                            self.options = []
                            return
                self.player_is_speeking = True
            else:
                self.player_is_speeking = False
        else:
            if self.player_is_speeking == False:
                self.text.render_all_text()

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
            screen.blit(self.title['title'], self.title['rect'])            
