import pygame
from settings import Settings
from font import LongText

dialog_texts = {
    "jon": [
        "hej", 
        "my name is jon. this is a long test. that i hopfully gining to skip to the next line. i will just keep typing shit untill the lenght is long enought. this is long enought. no this is longer.", 
        "godbye"
    ],
    "bob": "tjo",
    "jim": "Def",
    "else": "don't talk to me"
}

class Dialog:
    def __init__(self, text):
        self.settings = Settings()
        self.done = False
        self.text = text
        self.counter = 0
        self.get_image(self.text, self.counter)

    def get_image(self, text, counter):
        self.image = pygame.Surface((461, 150), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(centerx = self.settings.screen_width / 2, bottom = self.settings.screen_height)
        self.text_box = pygame.Rect((self.rect.x + 32, self.rect.y + 40),(self.rect.width - 32*2, self.rect.height - 40*2))
        url = 'assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Folding & Cutout/7 Dialogue Box/'
        src = '1_small.png' if counter < len(text) - 1 else '2_small.png'
        text = LongText(text[self.counter], self.text_box, has_underline=False)
        img = pygame.image.load(url + src).convert_alpha()
        self.image.blit(img, (0,0))
        self.image.blit(text.image, (42, 42))

    def update(self):
        pass

    def next(self):
        self.counter += 1
        if self.counter == len(self.text):
            self.done = True
        else:
            self.get_image(self.text, self.counter)

    def blitme(self, screen):
        screen.blit(self.image, self.rect)
