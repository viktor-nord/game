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
                    "A big one": {
                        "how big?": {
                            "100 m": None,
                            "5000 m": {
                                "oki doki": None
                            }
                        }
                    }
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
    def __init__(self, npc, player=None, animated=True):
        self.settings = Settings()
        self.done = False
        self.name = npc.id if npc else "else"
        self.title = self.name
        # self.text_array = dialog_texts['ulf']
        self.text_array = dialog_texts[self.name] if npc else dialog_texts["else"]
        self.counter = 0
        raw_text = next(iter(self.text_array[self.counter]))
        self.current_dialog = self.text_array[self.counter][raw_text]
        self.animated = animated
        self.text = self.new_text(raw_text)
        self.player_is_speeking = False
        self.options = None
        if npc:
            self.npc = self.get_char_img(npc, False)
        if player:
            self.player = self.get_char_img(player, True)

    def new_text(self, text):
        return DialogText(
            text,
            animated=True, 
            title=self.name,
            is_last_text=self.counter >= len(self.text_array) - 1
        )

    def get_char_img(self, char, is_player):
        img = char.character_sprite.display_image
        if is_player:
            center = self.text.rect.move(64, -16).topleft 
        else:
            center = self.text.rect.move(-64, -16).topright
        rect = img.get_rect(center=center)
        return {'img': img, 'rect': rect}

    def check_current_is_none(self):
        if self.current_dialog == None:
            return True
        if len(self.current_dialog) > 1:
            return False
        if self.current_dialog[next(iter(self.current_dialog))] == None:
            return True
        return False

    def check_to_render_text(self):
        if self.text.done or self.options:
            return False
        if self.player_is_speeking == False:
            return True
        return False

    def next_line(self):
        self.counter += 1
        self.current_dialog = self.text_array[self.counter]
        text = next(iter(self.current_dialog))
        self.text = self.new_text(text)

    def handle_options(self, val=None):
        click_val = val if val else self.options.handle_click()
        if click_val == None:
            return
        self.player_is_speeking = False
        self.options = None
        self.current_dialog = self.current_dialog[click_val]
        if self.current_dialog == None:
            self.next_line()
        else:
            text = next(iter(self.current_dialog))
            self.current_dialog = self.current_dialog[text]
            self.text = self.new_text(text)

    def handle_input(self, key):
        if key == pygame.K_SPACE:
            if self.options:
                index = self.options.pointer['index']
                options = [x['val'] for x in self.options.options]
                self.handle_options(options[index])
            else:
                self.next()

    def move_pointer(self, is_down):
        if self.options == None:
            return
        index = self.options.pointer['index']
        if is_down and index >= self.options.length - 1 or is_down == False and index == 0:
            return
        i = index + 1 if is_down else index - 1
        self.options.pointer['rect'].y = self.options.options[i]['rect'].y
        self.options.pointer['index'] = i

    def next(self):
        # if dialog is done but there is still text being typed
        if self.check_to_render_text():
            self.text.render_all_text()
            return
        # is last text and animation is done = dialog done
        if self.counter + 1 >= len(self.text_array):
            self.done = True
            return
        # check if there are more responces to current text in dialog tree
        if self.check_current_is_none():
            self.next_line()
        # check for options
        if len(self.current_dialog) > 1:
            self.options = DialogTextOptions(self.current_dialog, self.name)
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
        if self.options:
            self.options.blitme(screen)
        else:
            self.text.blitme(screen)

class DialogText:
    def __init__(self, text, animated=True, title=None, is_last_text=True):
        self.settings = Settings()
        self.done = False
        self.text = text
        self.animated = animated
        self.title = self.render_title(title) if title else None
        src = 'assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Folding & Cutout/7 Dialogue Box/'
        if is_last_text:
            self.image = pygame.image.load(src + '2_small.png').convert_alpha()
        else:
            self.image = pygame.image.load(src + '1_small.png').convert_alpha()
        w, h = self.settings.screen_width, self.settings.screen_height
        self.rect = self.image.get_rect(centerx=w/2, bottom=h)
        self.text_box = pygame.Rect(
            (self.rect.x + 32, self.rect.y + 50), 
            (self.rect.width - 32*2, self.rect.height - 50*2)
        )
        self.text = AnimatedText(text, self.text_box)

    def render_all_text(self):
        self.text.render_all_text()

    def render_title(self, title):
        holder = get_title_holder(98)
        surf, rect = holder['surf'], holder['rect']
        rect.centerx = self.settings.screen_width // 2
        rect.bottom = self.settings.screen_height - 8
        name = Text(title, rect, color=(223, 240, 216))
        surf.blit(name.text, name.relative_rect)
        return {'surf': surf, 'rect': rect}

    def update(self):
        if self.done:
            return
        if self.text.animation_done:
            self.done = True

    def blitme(self, screen):
        self.update()
        screen.blit(self.image, self.rect)
        self.text.blitme(screen)
        if self.title:
            screen.blit(self.title['surf'], self.title['rect'])

class DialogTextOptions(DialogText):
    def __init__(self, options, title):
        super().__init__("", animated=False, title=title, is_last_text=False)
        self.settings = Settings()
        self.options_val = options
        self.length = len(options)
        self.options = []
        wh = (self.text_box.width, self.text_box.height)
        self.surf = pygame.Surface(wh, pygame.SRCALPHA).convert_alpha()
        self.text_rect = self.text_box.copy()
        self.create_options(options)
        self.pointer = self.create_pointer()

    def create_pointer(self):
        arrow_image = pygame.image.load("assets/ui_sprites/Sprites/Content/4 Buttons/Sliced/5.png").convert_alpha()
        img = pygame.transform.flip(arrow_image, True, False)
        rect = img.get_rect(x = self.text_box.x, y = self.text_box.y)
        return {'image': img, 'rect': rect, 'index': 0}

    def create_options(self, options):
        x, y = 24, 17
        t = self.text_box
        for i, option in enumerate(options.keys()):
            r = pygame.Rect((t.x + x, t.y + y*i), (t.width, 20))
            text = Text(option, r)
            self.surf.blit(text.text, (x, y*i))
            self.options.append({'text': text.text, 'rect': r, 'val': option})

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        for op in self.options:
            if op['rect'].collidepoint(pos):
                return op['val']
        return None

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.text_box.collidepoint(pos):
            for i, option in enumerate(self.options):
                if option['rect'].collidepoint(pos):
                    self.pointer['rect'].y = option['rect'].y
                    self.pointer['index'] = i

    def blitme(self, screen):
        self.update()
        screen.blit(self.image, self.rect)
        screen.blit(self.surf, self.text_box)
        screen.blit(self.pointer['image'], self.pointer['rect'])
        if self.title:
            screen.blit(self.title['surf'], self.title['rect'])
