import pygame
from pathlib import Path
import json

from religion_page import ReligionPage
from page import Page
from nav_bar import NavBar
from race_page import RacePage
from general_page import GeneralPage
from ability_page import AbilityPage
from miracles_page import MiraclesPage
from submit_page import SubmitPage

class CharacterCreation(Page):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        # self.pages_completed = 0
        self.religion_page = ReligionPage(game)
        self.race_page = RacePage(game)
        self.general_page = GeneralPage(game)
        self.ability_page = AbilityPage(game)
        self.miracles_page = MiraclesPage(game)
        self.submit_page = SubmitPage(game)
        self.pages = ["general", "religion", "race", "ability", "miracles", "submit"]
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
        elif self.page == "miracles":
            self.miracles_page.update()
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
        elif self.page == "miracles":
            self.miracles_page.blitme(screen)
        elif self.page == "submit":
            self.submit_page.blitme(screen)
        else:
            self.general_page.blitme(screen)
        self.nav_bar.blitme(screen)

    def get_completed_amount(self):
        val = 0
        if self.general_page.complete:
            self.save_general()
            val += 1
        if self.religion_page.complete:
            val += 1
        if self.race_page.complete:
            val += 1
        if self.ability_page.complete:
            val += 1
        if self.miracles_page.complete:
            val += 1
        return val

    def save_general(self):
        with open(self.db_url, "r") as db:
            player = json.load(db)
        player["general"]["name"] = self.general_page.name
        player["general"]["age"] = self.general_page.age
        player["general"]["gender"] = self.general_page.gender
        with open(self.db_url, "w") as db:
            json.dump(player, db, indent=4)

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
        elif self.page == "miracles":
            self.miracles_page.check_click()
        elif self.page == "submit":
            self.submit_page.check_click()
        else:
            self.religion_page.check_click()
        completed = self.get_completed_amount()
        self.nav_bar.update_nav(completed)

    def handle_key(self, key):
        self.general_page.handle_key(key)
        completed = self.get_completed_amount()
        self.nav_bar.update_nav(completed)