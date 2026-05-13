import pygame

from page import Page
from font import Title, SmallTitle, Text
from button import CheckBoxList
from text_box import TextBox
from scroll_bar import ScrollBar

class ReligionPage(Page):
    def __init__(self, game):
        super().__init__()
        self.db_classes = self.get_db("data/classes.json")
        self.margin = 8
        self.complete = False
        self.init_class = self.db_classes["guru"]
        self.current_class = self.db_classes["guru"]
        # Left side
        self.left_title = Title(self.init_class["name"], self.left_title_container)
        self.stats_container = pygame.Rect(
            (self.left_page.left + self.margin, self.left_title_container.bottom + self.margin), 
            (100, 100)
        )
        self.render_text()
        # Right side
        self.right_title = Title("Practice", self.right_title_container)
        self.text_box_container = self.right_page.copy()
        info_text = "How you practice your faith effect everything from spells, abilities and personality. You can change your religion later."
        self.text_box = TextBox(info_text, self.text_box_container)
        self.text_box.rect.bottom = self.right_page.bottom
        r, th = self.right_page, self.right_title.rect.height
        self.check_box_container = pygame.Rect(
            (r.x, r.y + th + 16), (r.width, r.height - th - self.text_box.rect.height)
        )
        self.class_list = self.get_class_list()
        self.check_box_list = CheckBoxList(game, self.check_box_container, self.class_list)
        self.scroll_bar_container = pygame.Rect(
            (self.right_page.right - 16, self.right_title_container.bottom), 
            (16, self.check_box_container.height)
        )
        self.scroll_bar = ScrollBar(self.scroll_bar_container)

    def reset(self):
        player = self.get_db(self.player_url)
        if player["religion"]["practice"]:
            self.current_class = self.db_classes[player["religion"]["practice"]]
            self.render_text()

    def render_text(self):
        self.left_title = Title(self.current_class["name"], self.left_title_container)
        self.hp = SmallTitle(f"HP: {self.current_class["hit_die"]}", pos=self.stats_container.topleft)
        primary = self.stats_container.move(0, self.hp.rect.height + self.margin)
        self.primary_skill = Text(f"Primary: {self.current_class["primary_skill"]}", has_underline=True, size=20, is_bold=True, pos=primary.topleft)
        secondary = primary.move(0, self.primary_skill.rect.height + self.margin)
        self.secondary_skill = Text(f"Secondary: {self.current_class["secondary_skill"]}", has_underline=True, size=20, is_bold=True, pos=secondary.topleft)
        l, b = self.left_page, self.secondary_skill.rect.bottom
        self.desc_text_box_container = pygame.Rect((l.left, b + 4), (l.width, l.bottom - b - self.margin * 2))
        self.desc_text_box = TextBox(self.current_class["desc"], self.desc_text_box_container)

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

