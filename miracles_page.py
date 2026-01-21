import pygame
from pathlib import Path
import json

from page import Page
from font import PlainText, Title

class MiraclesPage(Page):
    def __init__(self, game):
        super().__init__(game)
        self.left_title = Title("Miracles", self.left_title_container)
        self.right_title = Title("Description", self.right_title_container)
        
    def check_click(self):
        pass
    def update(self):
        pass

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.left_title.image, self.left_title.rect)
        screen.blit(self.right_title.image, self.right_title.rect)
