import pygame

from page import Page
from font import Title, Text, LongText
from input import Input
from button import CheckBoxList

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
        self.name_input_container = pygame.Rect((self.right_page.left, self.right_title_container.bottom + 8), (self.right_page.width, 10))
        self.name_input = Input("name", "Name:", self.name_input_container)
        spacing = self.name_input.image.get_height() // 2
        self.name_input_container.height = self.name_input.image.get_height()
        self.name_input_container.y += spacing
        self.age = 0
        self.age_input_container = self.name_input_container.copy()
        self.age_input_container.top = self.name_input_container.bottom + spacing
        self.age_input = Input("age", "Age: ", self.age_input_container, only_numbers=True)
        self.gender = ""
        self.gender_label_container = pygame.Rect((self.right_page.left, self.age_input_container.bottom + spacing), (self.right_page.width, 10))
        self.gender_label = Text("Gender", self.gender_label_container, has_underline = True)
        self.gender_label_container.height = self.gender_label.image.get_height()
        self.gender_checkbox_container = self.gender_label_container.copy()
        self.gender_checkbox_container.top = self.gender_label_container.bottom
        gender_list = [
            {"id": "male", "text": "male", "value": "male"},
            {"id": "female", "text": "female", "value": "female"},
            {"id": "both", "text": "both", "value": "both"},
            {"id": "neither", "text": "neither", "value": "neither"},
        ]
        self.gender_checkbox = CheckBoxList(game, self.gender_checkbox_container,gender_list)
        self.complete = False

    def check_click(self):
        self.name_input.check_click()
        self.age_input.check_click()
        id = self.gender_checkbox.check_click()
        if id:
            self.gender = id
        self.check_if_done()

    def update(self):
        self.name_input.update()
        self.age_input.update()
        self.gender_checkbox.update()

    def handle_key(self, key):
        if self.name_input.is_active:
            name = self.name_input.handle_key(key)
            if name:
                self.name = name
        if self.age_input.is_active:
            age = self.age_input.handle_key(key)
            if age:
                self.age = age
        self.check_if_done()

    def check_if_done(self):
        if self.name != "" and self.age != 0 and self.gender != "":
            self.complete = True
        else:
            self.complete = False

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.right_title.image, self.right_title.rect)
        screen.blit(self.intro_text.image, self.intro_text_container)
        screen.blit(self.name_input.image, self.name_input_container)
        screen.blit(self.age_input.image, self.age_input_container)
        screen.blit(self.gender_label.image, self.gender_label.rect)
        self.gender_checkbox.draw_list(screen)
