import pygame
import pygame.font
from settings import Settings

def get_text_height(type="text"):
    if type == "text":
        size = 20
    elif type == "small title":
        size = 26
    elif type == "title":
        size = 42
    else:
        size = 20
    f = pygame.font.Font('assets/font/ThaleahFat.ttf', size)
    return f.render("Dummy text", True, (0,0,0)).convert_alpha().get_height()

class Text:
    def __init__(self, text, parent, size=20, has_underline=False, centered=True):
        pygame.font.init()
        self.has_underline = has_underline
        self.size = size
        self.parent = parent
        self.text_color = Settings().text_color
        self.font = pygame.font.Font('assets/font/ThaleahFat.ttf', size)
        self.under_line_img = pygame.image.load('assets/ui_sprites/Sprites/Content/5 Holders/20_2.png').convert_alpha()
        self.text = self.font.render(text, False, self.text_color).convert_alpha()
        self.image = pygame.Surface((self.text.get_width(), self.text.get_height()), pygame.SRCALPHA).convert_alpha()
        self.text_rect = self.text.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.text, (self.text_rect.x, self.text_rect.y))
        if centered:
            self.rect = self.text.get_rect(center=parent.center)
        else: 
            self.rect = self.text.get_rect(left = parent.left, top = parent.top)
        if has_underline:
            self.render_underline()

    def render_underline(self):
        x = 0
        y = self.image.get_height() - self.under_line_img.get_height()
        max_length = self.text_rect.width
        while x < max_length - self.under_line_img.get_width() - 5:
            self.image.blit(self.under_line_img, (x,y))
            x += self.under_line_img.get_width()
        self.image.blit(self.under_line_img, (max_length - self.under_line_img.get_width(), y))

    def blitme(self, screen):
        screen.blit(self.text, self.rect)

class Title(Text):
    def __init__(self, text, parent, size=42, has_underline=False):
        super().__init__(text, parent, size, has_underline, centered=True)
        self.font = pygame.font.Font('assets/font/Blackwood Castle.ttf', size)
        self.text = self.font.render(text, True, self.text_color)
        self.image = pygame.Surface((self.text.get_width(), self.text.get_height()), pygame.SRCALPHA)
        rect = self.text.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.text, (rect.x, rect.y))

class SmallTitle(Text):
    def __init__(self, text, parent, size=26, centered=True):
        super().__init__(text, parent, size, centered=centered, has_underline=True)
        self.under_line_img = pygame.image.load("assets/ui_sprites/Sprites/Content/5 Holders/19.png").convert_alpha()
        self.image = pygame.Surface((self.text.get_width(), self.text.get_height() + self.under_line_img.get_height() - 8), pygame.SRCALPHA)
        self.under_line_img_rect = self.under_line_img.get_rect(centerx=self.image.get_rect().centerx, bottom=self.image.get_rect().bottom)
        self.image.blit(self.text, self.text_rect)
        self.image.blit(self.under_line_img, self.under_line_img_rect)

class LongText(Text):
    def __init__(self, text, parent, animated=False, size=18):
        super().__init__(text, parent, size, has_underline=True, centered=False)
        self.text_string = text
        self.animated = animated
        self.width = parent.width
        self.text_list = self.get_text_list()
        self.height = len(self.text_list) * size + size
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(left = parent.left, top = parent.top)
        self.counter = 0
        if self.animated == False:
            self.render_text()

    def update(self):
        gg=0
    #     for i, word in enumerate(self.text_list):
    #         letter = self.font.render(
    #             [self.text_string[self.counter]], True, self.text_color
    #         )


    def render_text(self):
        x = 0
        under_line_x = 0
        y = 0
        for line_index, line in enumerate(self.text_list):
            for word in line:
                self.image.blit(word, (x, line_index * self.size))
                x += word.get_width()
            while under_line_x < self.width - 32:
                self.image.blit(self.under_line_img, (under_line_x, (line_index + 1) * self.size - 2))
                under_line_x += self.under_line_img.get_width() - 5
            self.image.blit(self.under_line_img, (self.width - self.under_line_img.get_width(), (line_index + 1) * self.size - 2))
            x = 0
            under_line_x = 0

    def get_text_list(self):
        list = [[]]
        string_list = self.text_string.split()
        line = 0
        x = 0
        for i, word in enumerate(string_list):
            val = word if i == len(string_list) - 1 else word  + " "
            t = self.font.render(val, False, self.text_color)
            if x + t.get_width() > self.width:
                list.append([t])
                line += 1
                x = 0
            else:
                list[line].append(t)
            x += t.get_width()
        return list