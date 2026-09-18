import pygame
from settings import Settings
from font import LongText

dialog_texts = {
    "jon": [
        "hej", 
        "my name is jon. this is a long test. that i hopfully gining to skip to the next line. i will just keep typing shit untill the lenght is long enought.", 
        "godbye"
    ],
    "bob": "tjo",
    "jim": "Def",
    "else": "don't talk to me"
}

class Dialog:
    def __init__(self, npc, player, animated=True):
        self.settings = Settings()
        self.done = False
        self.text_array = dialog_texts[npc.id] if npc else dialog_texts["else"]
        self.animated = animated
        self.counter = 0
        self.letter_counter = 0
        src = 'assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Folding & Cutout/7 Dialogue Box/'
        self.image = pygame.image.load(src + '1_small.png').convert_alpha()
        self.last_image = pygame.image.load(src + '2_small.png').convert_alpha()
        self.book_img = pygame.image.load('assets/ui_sprites/Sprites/Content/2 Icons/23.png').convert_alpha()
        self.rect = self.image.get_rect(centerx = self.settings.screen_width / 2, bottom = self.settings.screen_height)
        self.text_box = pygame.Rect((self.rect.x + 32, self.rect.y + 50),(self.rect.width - 32*2, self.rect.height - 50*2))
        self.get_text()
        self.npc = self.get_char_img(npc, False)
        self.player = self.get_char_img(player, True)

    def new_text(self, text):
        self.text_array = text
        self.counter = 0
        self.letter_counter = 0
        self.get_text()

    def get_text(self):
        if self.animated:
            t = self.text_array[self.counter][:self.letter_counter]
        else:
            t = self.text_array[self.counter]
        self.text = LongText(t, self.text_box, has_underline=False)

    def get_char_img(self, char, is_player):
        img = char.character_sprite.display_image
        center = self.rect.move(64, -16).topleft if is_player else self.rect.move(-64, -16).topright
        rect = img.get_rect(center=center)
        return {'img': img, 'rect': rect}

    def next(self):
        self.counter += 1
        self.letter_counter = 0
        if self.counter == len(self.text_array):
            self.done = True

    def update_text(self):
        self.letter_counter += 1
        self.text.__init__(self.text_array[self.counter][:self.letter_counter], self.text_box, has_underline=False)
        # self.text = LongText(self.text_array[self.counter][:self.letter_counter], self.text_box, has_underline=False)

    def blitme(self, screen):
        screen.blit(self.npc['img'], self.npc['rect'])
        screen.blit(self.player['img'], self.player['rect'])
        if self.counter < len(self.text_array):        
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.last_image, self.rect)
        if self.animated:
            self.update_text()
        screen.blit(self.text.image, self.text.rect)
        # pygame.draw.rect(screen, "red", self.rect)
