import pygame
from pathlib import Path
import json

from page import Page
from font import Title, SmallTitle, Text, LongText
from text_box import TextBox
from input import Input

class GeneralPage(Page):
    def __init__(self, game):
        super().__init__(game)
        margin = 8
        # Left side
        self.intro_text_container = self.left_page.copy()
        self.intro_text_container.left += margin
        self.intro_text_container.top += margin * 4
        self.intro_text_container.width -= margin * 2
        self.intro_text_container.height -= margin * 8
        self.intro_text = LongText(
            "Accustomed to life underground, you have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can't discern color in darkness, only shades of gray.",
            self.intro_text_container
        )
        # Right side
        self.right_title = Title("General", self.right_title_container)
        self.name = ""
        self.age = 0
        self.name_input_container = pygame.Rect((self.right_page.left, self.right_title_container.bottom + 8), (self.right_page.width, 10))
        self.name_input = Input("name", "Name:", self.name_input_container)
        self.name_input_container.height = self.name_input.image.get_height()
        self.age_input_container = self.name_input_container.copy()
        self.age_input_container.top = self.name_input_container.bottom
        self.age_input = Input("age", "Age: ", self.age_input_container, only_numbers=True)

    def check_click(self):
        self.name_input.check_click()
        self.age_input.check_click()

    def update(self):
        self.name_input.update()
        self.age_input.update()

    def handle_key(self, key):
        if self.name_input.is_active:
            name = self.name_input.handle_key(key)
            if name:
                self.name = name
        if self.age_input.is_active:
            age = self.age_input.handle_key(key)
            if age:
                self.age = age

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.right_title.image, self.right_title.rect)
        screen.blit(self.intro_text.image, self.intro_text_container)
        screen.blit(self.name_input.image, self.name_input_container)
        screen.blit(self.age_input.image, self.age_input_container)
