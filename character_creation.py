import pygame

from religion_page import ReligionPage
from page import Page
from nav_bar import NavBar
from race_page import RacePage
from general_page import GeneralPage
from ability_page import AbilityPage

class CharacterCreation(Page):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.religion_page = ReligionPage(game)
        self.race_page = RacePage(game)
        self.general_page = GeneralPage(game)
        self.ability_page = AbilityPage(game)
        self.magic_page = ReligionPage(game)
        self.submit_page = ReligionPage(game)
        self.pages = ["general", "religion", "race", "ability", "magic", "submit"]
        self.page = "general"
        self.nav_bar = NavBar()

    def update(self):
        if self.page == "general":
            self.general_page.update()
        elif self.page == "religion":
            self.religion_page.update()
        elif self.page == "race":
            self.race_page.update()
        elif self.page == "ability":
            self.ability_page.update()
        elif self.page == "magic":
            self.magic_page.update()
        elif self.page == "submit":
            self.submit_page.update()
        else:
            self.general_page.update()

    def blitme(self, screen):
        if self.page == "general":
            self.general_page.blitme(screen)
        elif self.page == "religion":
            self.religion_page.blitme(screen)
        elif self.page == "race":
            self.race_page.blitme(screen)
        elif self.page == "ability":
            self.ability_page.blitme(screen)
        elif self.page == "magic":
            self.magic_page.blitme(screen)
        elif self.page == "submit":
            self.submit_page.blitme(screen)
        else:
            self.general_page.blitme(screen)
        self.nav_bar.blitme(screen)

    def handle_click(self):
        self.nav_bar.handle_click()
        self.page = self.nav_bar.current
        if self.page == "general":
            self.general_page.check_click()
        elif self.page == "religion":
            self.religion_page.check_click()
        elif self.page == "race":
            self.race_page.check_click()
        elif self.page == "ability":
            self.ability_page.check_click()
        elif self.page == "magic":
            self.magic_page.check_click()
        elif self.page == "submit":
            self.submit_page.check_click()
        else:
            self.religion_page.check_click()

    def handle_key(self, key):
        self.general_page.handle_key(key)