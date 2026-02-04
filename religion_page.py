import pygame
from pathlib import Path
import json

from page import Page
from font import Title, SmallTitle, Text, get_text_height
from button import CheckBoxList
from text_box import TextBox
from scroll_bar import ScrollBar

class ReligionPage(Page):
    def __init__(self, game):
        super().__init__(game)
        self.db_classes = super().get_db("data/classes.json")
        margin = 8
        self.init_class = self.db_classes["guru"]
        self.current_class = self.db_classes["guru"]
        # Left side
        self.left_title = Title(self.init_class["name"], self.left_title_container)
        self.stats_container = pygame.Rect(
            (self.left_page.left + margin, self.left_title_container.bottom + margin), 
            ((self.left_page.width/2) - (margin*2), 100)
        )
        self.hp = SmallTitle(f"HP: {self.init_class["hit_die"]}", self.stats_container, centered=False)
        self.get_class_data(margin)
        self.complete = False

        # Right side
        self.right_title = Title("Practice", self.right_title_container)
        self.text_box_container = self.right_page.copy()
        info_text = "How you practice your faith effect everything from spells, abilities and personality. You can change your religion later."
        self.text_box = TextBox(info_text, self.text_box_container)
        self.text_box.rect.bottom = self.right_page.bottom

        self.check_box_container = self.right_page.copy()
        self.check_box_container.y += self.right_title.rect.height + 16
        self.check_box_container.height = self.right_page.height - self.right_title_container.height - self.text_box.rect.height
        self.class_list = self.get_class_list()
        self.check_box_list = CheckBoxList(
            game,
            self.check_box_container,
            self.class_list
        )
        self.scroll_bar_container = pygame.Rect(
            (self.right_page.right - 16, self.right_title_container.bottom), 
            (16, self.check_box_container.height)
        )
        self.scroll_bar = ScrollBar(self.scroll_bar_container)
        # self.render_text()

    def reset(self):
        player = super().get_db(self.player_url)
        if player["religion"]["practice"]:
            self.current_class = self.db_classes[player["religion"]["practice"]]
            self.render_text()

    def get_class_data(self, margin):
        self.primary_skill_container = self.stats_container.copy()
        self.primary_skill_container.y += self.hp.rect.height + margin
        self.primary_skill = Text(f"Primary: {self.init_class["primary_skill"]}", self.primary_skill_container, centered=False, has_underline=True)
        self.secondary_skill_container = self.primary_skill_container.copy()
        self.secondary_skill_container.y += self.primary_skill.rect.height + margin
        self.secondary_skill = Text(f"Secondary: {self.init_class["secondary_skill"]}", self.secondary_skill_container, centered=False, has_underline=True)
        self.desc_text_box_container = pygame.Rect(
            (self.left_page.left, self.secondary_skill.rect.bottom + margin * 4),
            (self.left_page.width, self.left_page.bottom - self.secondary_skill.rect.bottom - margin*2)
        )
        self.desc_text_box = TextBox(self.init_class["desc"], self.desc_text_box_container)
        self.desc_text_box.rect.center = self.desc_text_box_container.center

    def render_text(self):
        self.left_title = Title(self.current_class["name"], self.left_title_container)
        self.hp = SmallTitle(f"HP: {self.current_class["hit_die"]}", self.stats_container, centered=False)
        self.primary_skill = Text(f"Primary: {self.current_class["primary_skill"]}", self.primary_skill_container, centered=False, has_underline=True)
        self.secondary_skill = Text(f"Secondary: {self.current_class["secondary_skill"]}", self.secondary_skill_container, centered=False, has_underline=True)
        self.desc_text_box = TextBox(self.current_class["desc"], self.desc_text_box_container)
        self.desc_text_box.rect.center = self.desc_text_box_container.center

    def get_class_list(self):
        arr = []
        for key, value in self.db_classes.items():
            arr.append({"id": key, "text": value["name"], "value": key})
        return arr

    def check_click(self):
        id = self.check_box_list.check_click()
        if id:
            self.current_class = self.db_classes[id]
            self.complete = True
            self.render_text()

    def update(self):
        self.check_box_list.update()

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.right_title.image, self.right_title.rect)
        screen.blit(self.left_title.image, self.left_title.rect)
        self.check_box_list.draw_list(screen)
        screen.blit(self.scroll_bar.image, self.scroll_bar.rect)
        screen.blit(self.text_box.image, self.text_box.rect)
        screen.blit(self.hp.image, self.hp.rect)
        screen.blit(self.primary_skill.image, self.primary_skill.rect)
        screen.blit(self.secondary_skill.image, self.secondary_skill.rect)
        screen.blit(self.desc_text_box.image, self.desc_text_box.rect)

