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

class NoPage:
    def __init__(self):
        self.complete = False

class CharacterCreation(Page):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.name = "character_creation"
        self.pages = {
            "general": GeneralPage(), 
            "religion": NoPage(), 
            "race": NoPage(), 
            "ability": NoPage(), 
            "miracles": NoPage(), 
            "submit": NoPage()
        }
        self.page = "general"
        self.nav_bar = NavBar()

    def update(self):
        self.pages[self.page].update()
        completed_amount = sum([val.complete for val in self.pages.values()])
        new_page = self.nav_bar.update_nav(completed_amount)
        if new_page:
            self.load_new_page(new_page)

    def blitme(self, screen):
        self.pages[self.page].blitme(screen)
        self.nav_bar.blitme(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click()
        elif event.type == pygame.KEYDOWN:
            self.handle_key(event.key)

    def handle_click(self):
        self.nav_bar.handle_click()
        if self.page != self.nav_bar.current:
            self.handle_save(self.page)
        self.page = self.nav_bar.current
        self.pages[self.page].check_click()

    def handle_key(self, key):
        self.pages["general"].handle_key(key)

    def load_new_page(self, new_page):
        if new_page == "religion":
            self.pages["religion"] = ReligionPage()
        if new_page == "race":
            self.pages["race"] = RacePage()
        if new_page == "ability":
            self.pages["ability"] = AbilityPage()
        if new_page == "miracles":
            self.pages["miracles"] = MiraclesPage()
        if new_page == "submit":
            self.pages["submit"] = SubmitPage()

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
        player = self.get_db("save/player.json")
        player["general"]["name"] = self.pages["general"].name
        player["general"]["age"] = self.pages["general"].age
        player["general"]["gender"] = self.pages["general"].gender
        self.save(player)

    def save_religion(self):
        player = self.get_db("save/player.json")
        player["religion"]["practice"] = self.pages["religion"].current_class["name"]
        player["religion"]["hit_die"] = self.pages["religion"].current_class["hit_die"]
        self.save(player)

    def save_race(self):
        player = self.get_db("save/player.json")
        player["general"]["race"] = self.pages["race"].current_race["name"]
        player["general"]["speed"] = self.pages["race"].current_race["speed"]
        player["general"]["size"] = self.pages["race"].current_race["size"]
        trait_list = [trait["name"] for trait in self.pages["race"].current_race["traits"]]
        player["general"]["traits"] = trait_list
        self.save(player)

    def save_ability(self):
        player = self.get_db("save/player.json")
        player["stats"]["strength"] = self.get_ability_value(0)
        player["stats"]["wisdom"] = self.get_ability_value(1)
        player["stats"]["constitution"] = self.get_ability_value(2)
        player["stats"]["dexterity"] = self.get_ability_value(3)
        player["stats"]["intelligence"] = self.get_ability_value(4)
        player["stats"]["charisma"] = self.get_ability_value(5)
        player["proficiencies"] = self.pages["ability"].selected_proficiencies
        self.save(player)

    def get_ability_value(self, index):
        a = self.pages["ability"].abilities[index]
        return a.values[a.value_index] + a.bonus
    
    def save_miracles(self):
        pass
        # player = self.load()
        # self.save(player)

    def save(self, player):
        with open("save/player.json", "w") as db:
            json.dump(player, db, indent=4)

