import pygame
from pathlib import Path
import json
import math

from religion_page import ReligionPage
from page import Page
from nav_bar import NavBar
from race_page import RacePage
from general_page import GeneralPage
from ability_page import AbilityPage
from miracles_page import MiraclesPage
from submit_page import SubmitPage

class NoPage:
    def __init__(self):
        self.complete = False

class CharacterCreation(Page):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.religion_page = ReligionPage(self.game)
        self.race_page = RacePage(self.game)
        self.ability_page = AbilityPage(self.game)
        self.miracles_page = MiraclesPage(self.game)
        self.submit_page = SubmitPage(self.game)
        # self.pages_completed = 0
        self.general_page = GeneralPage(game)
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

    def handle_save(self, page):
        if page == "general":
            self.save_general()
        elif page == "religion":
            self.save_religion()
        elif page == "race":
            self.save_race()
        elif page == "ability":
            self.save_ability()
        elif page == "miracles":
            self.save_miracles()
        else:
            print("something wrong in handle_save()")

    def save_general(self):
        player = self.get_save()
        player["general"]["name"] = self.general_page.name
        player["general"]["age"] = self.general_page.age
        player["general"]["gender"] = self.general_page.gender
        self.save(player)

    def save_religion(self):
        player = self.get_save()
        player["religion"]["practice"] = self.religion_page.current_class["name"]
        player["religion"]["hit_die"] = self.religion_page.current_class["hit_die"]
        self.save(player)

    def save_race(self):
        player = self.get_save()
        player["general"]["race"] = self.race_page.current_race["name"]
        player["general"]["speed"] = self.race_page.current_race["speed"]
        player["general"]["size"] = self.race_page.current_race["size"]
        trait_list = []
        for trait in self.race_page.current_race["traits"]:
            trait_list.append(trait["name"])
        player["general"]["traits"] = trait_list
        self.save(player)

    def save_ability(self):
        player = self.get_save()
        str = self.get_ability_value(0)
        wis = self.get_ability_value(1)
        con = self.get_ability_value(2)
        dex = self.get_ability_value(3)
        int = self.get_ability_value(4)
        cha = self.get_ability_value(5)
        player["stats"]["strength"] = str
        player["stats"]["wisdom"] = wis
        player["stats"]["constitution"] = con
        player["stats"]["dexterity"] = dex
        player["stats"]["intelligence"] = int
        player["stats"]["charisma"] = cha
        player["stats"]["strength_modifier"] = self.calc_modifier(str)
        player["stats"]["wisdom_modifier"] = self.calc_modifier(wis)
        player["stats"]["constitution_modifier"] = self.calc_modifier(con)
        player["stats"]["dexterity_modifier"] = self.calc_modifier(dex)
        player["stats"]["intelligence_modifier"] = self.calc_modifier(int)
        player["stats"]["charisma_modifier"] = self.calc_modifier(cha)
        player["proficiencies"] = self.ability_page.selected_proficiencies
        self.save(player)

    def get_ability_value(self, index):
        a = self.ability_page.abilities[index]
        return a.values[a.value_index] + a.bonus
    
    def calc_modifier(self, stat):
        val = (stat - 10) / 2
        return math.floor(val)

    def save_miracles(self):
        pass
        # player = self.load()
        # self.save(player)

    def get_save(self):
        with open("save/player.json", "r") as db:
            return json.load(db)

    def save(self, player):
        with open("save/player.json", "w") as db:
            json.dump(player, db, indent=4)

    def reset_next_page(self, page):
        if page == "general":
            pass
            # self.general_page.reset()
        elif page == "religion":
            pass
            # self.religion_page.reset()
        elif page == "race":
            pass
            # self.race_page.reset()
        elif page == "ability":
            self.ability_page.reset()
        elif page == "miracles":
            self.miracles_page.reset()
        elif page == "submit":
            pass
            # self.submit_page.reset()
        else:
            pass

    def handle_click(self):
        self.nav_bar.handle_click()
        if self.page != self.nav_bar.current:
            self.handle_save(self.page)
            self.reset_next_page(self.nav_bar.current)  
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
        # completed = self.get_completed_amount()
        # self.nav_bar.update_nav(completed)

    def handle_key(self, key):
        self.general_page.handle_key(key)
        # completed = self.get_completed_amount()
        # self.nav_bar.update_nav(completed)