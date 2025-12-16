import pygame
from pathlib import Path
import json

from page import Page
from font import Title
from button import CheckBoxList
from text_box import TextBox

class ReligionPage(Page):
    def __init__(self, game):
        super().__init__(game)
        classes_path = Path("data/classes.json")
        self.db_classes = json.loads(classes_path.read_text())
        self.right_title = Title("Faith", self.right_title_container)
        self.left_title = Title("Info", self.left_title_container)
        self.check_box_container = self.right_page.copy()
        margin = self.right_title.rect.height + 16
        self.check_box_container.y += margin
        self.check_box_container.height -= margin
        self.class_list = self.get_class_list()
        self.check_box_list = CheckBoxList(
            self.game, 
            self.check_box_container,
            self.class_list
        )
        self.text_box_container = self.left_page.copy()
        self.text_box_container.height = 100
        self.text_box_container.y += 50
        self.text_box = TextBox(self.game, "this is a test text for the purpus of checking the lenght and height of the text box. now i m making the text box bigger", self.text_box_container)
    
    def get_class_list(self):
        arr = []
        for key, value in self.db_classes.items():
            arr.append({"id": key, "text": value["name"], "data": value})
        return arr

    def update(self):
        self.check_box_list.update()

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.right_title.image, self.right_title.rect)
        screen.blit(self.left_title.image, self.left_title.rect)
        self.check_box_list.draw_list(screen)

