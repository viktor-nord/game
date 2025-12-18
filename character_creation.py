import pygame

from religion_page import ReligionPage
from page import Page
from nav_bar import NavBar
from race_page import RacePage

class CharacterCreation(Page):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.religion_page = ReligionPage(game)
        self.race_page = RacePage(game)
        self.pages = ["general","religion", "rase"]
        self.page = "religion"
        self.nav_bar = NavBar()

    def update(self):
        if self.page == "religion":
            self.religion_page.update()
        elif self.page == "race":
            self.race_page.update()
        else:
            self.religion_page.update()

    def blitme(self, screen):
        if self.page == "religion":
            self.religion_page.blitme(screen)
        elif self.page == "race":
            self.race_page.blitme(screen)
        else:
            self.religion_page.blitme(screen)
        self.nav_bar.blitme(screen)

    def handle_click(self):
        self.nav_bar.handle_click()
        self.page = self.nav_bar.current
        if self.page == "religion":
            self.religion_page.check_click()
        elif self.page == "race":
            self.race_page.check_click()
        else:
            self.religion_page.check_click()