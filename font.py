from turtle import left

import pygame
import pygame.font
from settings import Settings

class PlainText:
    def __init__(self, text, size=18, color=None):
        pygame.font.init()
        self.size = size
        self.text_color = color if color else Settings().text_color
        self.font = pygame.font.Font('assets/font/ThaleahFat.ttf', size)
        self.text = self.font.render(text, False, self.text_color).convert_alpha()
        self.image = self.text
        self.rect = self.text.get_rect()

    def blitme(self, screen):
        screen.blit(self.image, self.rect)

class Text:
    def __init__(self, text, parent=None, size=18, has_underline=False, is_bold=True, color=None, pos=None):
        pygame.font.init()
        self.text_color = color if color else Settings().text_color
        src = 'assets/font/ThaleahFat.ttf' if is_bold else 'assets/font/Barlow-Black.ttf'
        self.font = pygame.font.Font(src, size)
        smooth_render = not is_bold
        self.text = self.font.render(text, smooth_render, self.text_color).convert_alpha()
        wh = (self.text.get_width(), self.text.get_height())
        self.image = pygame.Surface(wh, pygame.SRCALPHA).convert_alpha()
        self.image.blit(self.text, (0,0))
        self.under_line_img = pygame.image.load(
            'assets/ui_sprites/Sprites/Content/5 Holders/20_2.png'
        ).convert_alpha()
        if parent:
            self.rect = self.image.get_rect(center = parent.center)
            self.relative_rect = self.image.get_rect(center = (parent.width / 2, parent.height / 2))
        elif pos:
            self.rect = self.image.get_rect(left = pos[0], top = pos[1])
            self.relative_rect = self.image.get_rect(left = pos[0], top = pos[1])            
        else:
            self.rect = self.image.get_rect()
            self.relative_rect = self.image.get_rect()
        if has_underline:
            self.render_underline()

    def render_underline(self):
        w = self.under_line_img.get_width()
        x = 0
        y = self.image.get_height() - self.under_line_img.get_height()
        max_length = self.text.get_width()
        while x < max_length - w - 5:
            self.image.blit(self.under_line_img, (x,y))
            x += w
        self.image.blit(self.under_line_img, (max_length - w, y))

    def blitme(self, screen):
        screen.blit(self.text, self.rect)

class Title(Text):
    def __init__(self, text, parent, size=42, has_underline=False):
        super().__init__(text, parent, size, has_underline)
        self.font = pygame.font.Font('assets/font/Blackwood Castle.ttf', size)
        self.text = self.font.render(text, True, self.text_color)
        self.image = pygame.Surface((self.text.get_width(), self.text.get_height()), pygame.SRCALPHA)
        rect = self.text.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.text, (rect.x, rect.y))

class SmallTitle(Text):
    def __init__(self, text, parent=None, size=26, pos=None):
        super().__init__(text, parent=parent, size=size, has_underline=True, is_bold=True, pos=pos)
        self.under_line_img = pygame.image.load("assets/ui_sprites/Sprites/Content/5 Holders/19.png").convert_alpha()
        self.image = pygame.Surface((self.text.get_width(), self.text.get_height() + self.under_line_img.get_height() - 8), pygame.SRCALPHA)
        r = self.image.get_rect()
        under_line_img_rect = self.under_line_img.get_rect(centerx = r.centerx, bottom = r.bottom)
        self.image.blit(self.text, (0,0))
        self.image.blit(self.under_line_img, under_line_img_rect)

class LongText(Text):
    def __init__(self, text, parent, animated=False, size=18, has_underline=True):
        super().__init__(text, parent, size=size, has_underline=has_underline, is_bold=False)
        self.text_string = text
        self.has_underline = has_underline
        self.animated = animated
        self.width = parent.width
        self.size = size
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
            if self.has_underline:
                while under_line_x < self.width - 32:
                    self.image.blit(self.under_line_img, (under_line_x, (line_index + 1) * self.size))
                    under_line_x += self.under_line_img.get_width() - 5
                self.image.blit(self.under_line_img, (self.width - self.under_line_img.get_width(), (line_index + 1) * self.size))
            x = 0
            under_line_x = 0

    def get_text_list(self):
        list = [[]]
        string_list = self.text_string.split()
        line = 0
        x = 0
        for i, word in enumerate(string_list):
            val = word if i == len(string_list) - 1 else word  + " "
            t = self.font.render(val, True, self.text_color)
            if x + t.get_width() > self.width:
                list.append([t])
                line += 1
                x = 0
            else:
                list[line].append(t)
            x += t.get_width()
        return list