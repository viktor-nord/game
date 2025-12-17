import pygame

from religion_page import ReligionPage

class CharacterCreation:
    def __init__(self, game):
        self.game = game
        self.religion_page = ReligionPage(game)
        self.pages = ["general","religion", "rase"]
        self.page = "religion"

    def update(self):
        if self.page == "religion":
            self.religion_page.update()

    def blitme(self, screen):
        if self.page == "religion":
            self.religion_page.blitme(screen)

    def handle_click(self):
        if self.page == "religion":
            self.religion_page.check_click()