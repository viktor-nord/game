from csv import Error
from turtle import left
import pygame
from pathlib import Path
import json

from page import Page
from font import Title, SmallTitle, Text
from button import CheckBoxList
from text_box import TextBox
from scroll_bar import ScrollBar

class RacePage(Page):
    def __init__(self, game):
        super().__init__(game)
        rases_path = Path("data/rases.json")
        self.db_races = json.loads(rases_path.read_text())
        self.current_race = self.db_races["dwarf"]
        margin = 8
        # Left side
        self.left_title = Title(self.current_race["name"], self.left_title_container)
        self.size_container = self.left_page.copy()
        self.size_container.top = self.left_title_container.bottom + margin
        self.size_container.left += margin
        self.size_text = Text(f"Size: {self.current_race["size"]}", self.size_container, has_underline=False, centered=False)
        self.size_container.height = self.size_text.image.get_height()
        self.speed_container = self.size_container.copy()
        self.speed_container.top = self.size_container.bottom
        self.speed_text = Text(f"Speed: {self.current_race["speed"]}", self.speed_container, has_underline=False, centered=False)
        self.get_abi()
        self.get_traits()

        # Right side
        self.right_title = Title("Race", self.right_title_container)
        self.text_box_container = self.right_page.copy()
        info_text = "Race effect everything from spells, abilities and personality. You can change your religion later."
        self.text_box = TextBox(info_text, self.text_box_container)
        self.text_box.rect.bottom = self.right_page.bottom
        self.check_box_container = self.right_page.copy()
        self.check_box_container.y += self.right_title.rect.height + 16
        self.check_box_container.height = self.right_page.height - self.right_title_container.height - self.text_box.rect.height
        self.race_list = self.get_race_list()
        self.check_box_list = CheckBoxList(
            game,
            self.check_box_container,
            self.race_list
        )
        self.render_text()

    def get_abi(self):
        self.abi_container = self.speed_container.copy()
        self.abi_container.top = self.speed_container.bottom
        name = self.current_race["abs"][0]["name"]
        if self.current_race["name"] == "human":
            name = "all"
        text = f"Ability Increase: {name} + {self.current_race["abs"][0]["val"]}"
        self.abi_text = Text(text, self.abi_container, has_underline=False, centered=False)
        self.abi_container_2 = self.abi_container.copy()
        self.abi_container_2.top = self.abi_container.bottom
        if len(self.current_race["abs"]) > 1 and self.current_race["name"] != "human":
            text_2 = f"Ability Increase: {self.current_race["abs"][1]["name"]} + {self.current_race["abs"][1]["val"]}"
            self.abi_text_2 = Text(text_2, self.abi_container, has_underline=False, centered=False)
        else:
            self.abi_text_2 = None

    def get_traits(self):
        self.traits_title_container = self.left_page.copy()
        self.traits_title_container.height = 30
        self.traits_title_container.top = self.abi_container_2.bottom
        self.traits_title = Text("Traits", self.traits_title_container, size=22)

        self.traits_surf = pygame.Surface((
            self.left_page.right - self.left_page.left, 
            self.left_page.bottom - self.traits_title_container.bottom + 8
        ), pygame.SRCALPHA).convert_alpha()
        self.traits_rect = self.traits_surf.get_rect(top=self.traits_title_container.bottom + 8, left=self.left_page.left)
        traits_list = self.current_race["traits"]
        for i, trait in enumerate(traits_list):
            p = self.traits_surf.get_rect()
            if i == 1:
                p = self.traits_surf.get_rect(left = self.traits_rect.width // 2)
            if i == 2:
                p = self.traits_surf.get_rect(top = 30)
            if i == 3:
                p = self.traits_surf.get_rect(left = self.traits_rect.width // 2, top = 30)
            t = Text(trait["name"], p, has_underline=True, centered=False)
            self.traits_surf.blit(t.image, t.rect)

    def render_text(self):
        self.left_title = Title(self.current_race["name"], self.left_title_container)
        self.size_text = Text(f"Size: {self.current_race["size"]}", self.size_container, has_underline=False, centered=False)
        self.speed_text = Text(f"Speed: {self.current_race["speed"]}", self.speed_container, has_underline=False, centered=False)
        self.get_abi()
        self.get_traits()

    def get_race_list(self):
        arr = []
        for key, value in self.db_races.items():
            arr.append({"id": key, "text": value["name"], "value": key})
        return arr

    def check_click(self):
        id = self.check_box_list.check_click()
        if id:
            self.current_race = self.db_races[id]
            self.render_text()

    def update(self):
        gg=0
        # self.check_box_list.update()

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.right_title.image, self.right_title.rect)
        screen.blit(self.left_title.image, self.left_title.rect)
        self.check_box_list.draw_list(screen)
        screen.blit(self.text_box.image, self.text_box.rect)
        screen.blit(self.size_text.image, self.size_container)
        screen.blit(self.speed_text.image, self.speed_container)
        screen.blit(self.abi_text.image, self.abi_container)
        screen.blit(self.traits_surf, self.traits_rect)
        screen.blit(self.traits_title.image, self.traits_title.rect)
        try:
            screen.blit(self.abi_text_2.image, self.abi_container_2)
        except AttributeError:
            do_nothing = True
