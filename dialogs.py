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
    def __init__(self, text, animated=True):
        self.settings = Settings()
        self.done = False
        self.text_array = text
        self.animated = animated
        self.counter = 0
        self.letter_counter = 0
        self.image = pygame.image.load('assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Folding & Cutout/7 Dialogue Box/1_small.png').convert_alpha()
        self.last_image = pygame.image.load('assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Folding & Cutout/7 Dialogue Box/2_small.png').convert_alpha()
        self.rect = self.image.get_rect(centerx = self.settings.screen_width / 2, bottom = self.settings.screen_height)
        self.text_box = pygame.Rect((self.rect.x + 32, self.rect.y + 50),(self.rect.width - 32*2, self.rect.height - 50*2))
        self.get_text()

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
        if self.counter < len(self.text_array):        
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.last_image, self.rect)
        if self.animated:
            self.update_text()
        screen.blit(self.text.image, self.text.rect)
