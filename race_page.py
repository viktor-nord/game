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
        self.db_rases = json.loads(rases_path.read_text())
        margin = 8
        # Left side
        self.left_title = Title("Hello", self.left_title_container)

        # Right side
        self.right_title = Title("Race", self.right_title_container)
        self.text_box_container = self.right_page.copy()
        info_text = "Race effect everything from spells, abilities and personality. You can change your religion later."
        self.text_box = TextBox(self.game, info_text, self.text_box_container)
        self.text_box.rect.bottom = self.right_page.bottom
        # self.check_box_container = self.right_page.copy()
        # margin = self.right_title.rect.height + 16
        # self.check_box_container.y += margin
        # self.check_box_container.height = self.right_page.height - self.right_title_container.height - self.text_box.rect.height
        # self.class_list = self.get_class_list()
        # self.check_box_list = CheckBoxList(
        #     self.game, 
        #     self.check_box_container,
        #     self.class_list
        # )
        # self.scroll_bar_container = pygame.Rect(
        #     (self.right_page.right - 16, self.right_title_container.bottom), 
        #     (16, self.right_page.height - self.right_title_container.height - self.text_box_container.height)
        # )
        # self.scroll_bar = ScrollBar(self.scroll_bar_container)
        # self.render_text()

    # def render_text(self):
    #     self.left_title = Title(self.current_class["name"], self.left_title_container)
    #     self.hp = SmallTitle(f"HP: {self.current_class["hit_die"]}", self.stats_container, centered=False)
    #     self.primary_skill = Text(f"Primary: {self.current_class["primary_skill"]}", self.primary_skill_container, centered=False, has_underline=True)
    #     self.secondary_skill = Text(f"Secondary: {self.current_class["secondary_skill"]}", self.secondary_skill_container, centered=False, has_underline=True)
    #     self.desc_text_box = TextBox(self.game, self.current_class["desc"], self.desc_text_box_container)
    #     self.desc_text_box.rect.center = self.desc_text_box_container.center

    # def get_class_list(self):
    #     arr = []
    #     for key, value in self.db_classes.items():
    #         arr.append({"id": key, "text": value["name"], "value": key})
    #     return arr

    def check_click(self):
        gg=0
    #     id = self.check_box_list.check_click()
    #     if id:
    #         self.current_class = self.db_classes[id]
    #         self.render_text()
    #     # self.left_title = Title(self.current_class["name"], self.left_title_container)
    #     # self.hp = SmallTitle(f"HP: {self.current_class["hit_die"]}", self.stats_container, centered=False)
    #     # self.primary_skill = Text(f"Primary: {self.current_class["primary_skill"]}", self.primary_skill_container, centered=False, has_underline=True)
    #     # self.secondary_skill = Text(f"Secondary: {self.current_class["secondary_skill"]}", self.secondary_skill_container, centered=False, has_underline=True)
    #     # self.desc_text_box = TextBox(self.game, self.current_class["desc"], self.desc_text_box_container)

    def update(self):
        gg=0
        # self.check_box_list.update()

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.right_title.image, self.right_title.rect)
        screen.blit(self.left_title.image, self.left_title.rect)
        # self.check_box_list.draw_list(screen)
        # screen.blit(self.scroll_bar.image, self.scroll_bar.rect)
        screen.blit(self.text_box.image, self.text_box.rect)
        # screen.blit(self.hp.image, self.hp.rect)
        # screen.blit(self.primary_skill.image, self.primary_skill.rect)
        # screen.blit(self.secondary_skill.image, self.secondary_skill.rect)
        # screen.blit(self.desc_text_box.image, self.desc_text_box.rect)
        # pygame.draw.rect(screen, "red", self.desc_text_box_container)

