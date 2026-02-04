import pygame
from pathlib import Path
import json

from page import Page
from font import PlainText, Title, SmallTitle, Text
from button import CheckBoxList
from text_box import TextBox
from scroll_bar import ScrollBar


class MiraclesPage(Page):
    def __init__(self, game):
        super().__init__(game)
        self.right_title = Title("Miracles", self.right_title_container)
        self.complete = False
        self.cantrip_url = "data/miracles/cantrips.json"

        self.non_magic_users = ["priest", "martyr", "monk", "virgin", "none"]
        self.db_cantrip = self.get_cantrips()
        self.db_lv1 = super().get_db("data/miracles/lv1.json")
        margin = 8
        self.display_spell = self.db_cantrip[0] 
        # Left side
        self.left_title = Title(self.display_spell["name"], self.left_title_container)
        self.stats_container = pygame.Rect(
            (self.left_page.left + margin, self.left_title_container.bottom + margin), 
            ((self.left_page.width/2) - (margin*2), 100)
        )
        self.range = SmallTitle(f"Range: {self.display_spell["range"]}", self.stats_container, centered=False)
        self.get_miracle_info(margin)
        # Right side
        # self.text_box_container = self.right_page.copy()
        # info_text = "How you practice your faith effect everything from spells, abilities and personality. You can change your religion later."
        # self.text_box = TextBox(info_text, self.text_box_container)
        # self.text_box.rect.bottom = self.right_page.bottom
        self.check_box_container = self.right_page.copy()
        self.check_box_container.y += self.right_title.rect.height
        # self.check_box_container.height = self.right_page.height - self.right_title_container.height - self.text_box.rect.height
        self.spell_list = self.get_spell_list()
        self.check_box_list = CheckBoxList(
            game,
            self.check_box_container,
            self.spell_list
        )
        self.scroll_bar_container = pygame.Rect(
            (self.right_page.right - 16, self.right_title_container.bottom), 
            (16, self.right_page.height - self.right_title_container.height - 16)
        )
        self.scroll_bar = ScrollBar(self.scroll_bar_container)
        self.render_text()

    def get_cantrips(self):
        val = []
        arr = super().get_db(self.cantrip_url)
        player = super().get_db(self.player_url)
        faith = player["religion"]["practice"]
        if faith in self.non_magic_users:
            val.append(arr[0])
        else:
            for spell in arr:
                if faith in spell["classes"]:
                    val.append(spell)
        return val 

    def reset(self):
        self.db_cantrip = self.get_cantrips()
        self.render_text()

    def get_spell_list(self):
        arr = []
        for value in self.db_cantrip:
            t = value["name"]
            if len(t) > 7:
                t = value["name"][:7] + "..."
            arr.append({"id": value["name"], "text": t, "value": value["name"]})
        return arr
        
    def get_miracle_info(self, margin):
        self.primary_skill_container = self.stats_container.copy()
        self.primary_skill_container.y += self.range.rect.height + margin
        self.primary_skill = Text(
            f"Casting Time: {self.display_spell["casting_time"]}", 
            self.primary_skill_container, 
            centered=False, 
            has_underline=True
        )
        self.secondary_skill_container = self.primary_skill_container.copy()
        self.secondary_skill_container.y += self.primary_skill.rect.height + margin
        self.secondary_skill = Text(
            f"Duration: {self.display_spell["duration"]}", 
            self.secondary_skill_container, 
            centered=False, 
            has_underline=True
        )
        self.desc_text_box_container = pygame.Rect(
            (self.left_page.left, self.secondary_skill.rect.bottom + margin * 4),
            (self.left_page.width, self.left_page.bottom - self.secondary_skill.rect.bottom - margin*2)
        )
        self.desc_text_box = TextBox(self.display_spell["desc"], self.desc_text_box_container)
        self.desc_text_box.rect.center = self.desc_text_box_container.center

    def render_text(self):
        self.left_title = Title(self.display_spell["name"], self.left_title_container)
        self.range = SmallTitle(f"Range: {self.display_spell["range"]}", self.stats_container, centered=False)
        self.primary_skill = Text(
            f"Casting Time: {self.display_spell["casting_time"]}", 
            self.primary_skill_container, 
            centered=False, 
            has_underline=True
        )
        self.secondary_skill = Text(
            f"Duration: {self.display_spell["duration"]}", 
            self.secondary_skill_container, 
            centered=False, 
            has_underline=True
        )
        self.desc_text_box = TextBox(self.display_spell["desc"], self.desc_text_box_container)
        self.desc_text_box.rect.center = self.desc_text_box_container.center


    def check_click(self):
        id = self.check_box_list.check_click()
        if id:
            for spell in self.db_cantrip:
                if spell["name"] == id:
                    self.display_spell = spell
            self.complete = True
            self.render_text()

    def update(self):
        self.check_box_list.update()

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.left_title.image, self.left_title.rect)
        screen.blit(self.right_title.image, self.right_title.rect)

        screen.blit(self.right_title.image, self.right_title.rect)
        screen.blit(self.left_title.image, self.left_title.rect)
        self.check_box_list.draw_list(screen)
        screen.blit(self.scroll_bar.image, self.scroll_bar.rect)
        # screen.blit(self.text_box.image, self.text_box.rect)
        screen.blit(self.range.image, self.range.rect)
        screen.blit(self.primary_skill.image, self.primary_skill.rect)
        screen.blit(self.secondary_skill.image, self.secondary_skill.rect)
        screen.blit(self.desc_text_box.image, self.desc_text_box.rect)
