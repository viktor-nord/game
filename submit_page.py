import pygame
from pathlib import Path
import json

from page import Page
from font import PlainText, Title
from button import Button

class SubmitPage(Page):
    def __init__(self, game):
        super().__init__(game)
        self.left_title = Title("You", self.left_title_container)
        self.submit_button = Button(game, "submit", "Submit", self.right_page, "submit")
        self.submit_button.rect.center = self.right_page.center

    def check_click(self):
        pass
    def update(self):
        pass

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.left_title.image, self.left_title.rect)
        screen.blit(self.submit_button.image, self.submit_button.rect)
