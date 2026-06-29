import pygame

from page import Page
from font import Title, SmallTitle, Text
from button import Button, CheckBoxList
from text_box import TextBox
from scroll_bar import ScrollBar


class MiraclesPage(Page):
    def __init__(self):
        super().__init__()
        self.right_title = Title("Miracles", self.right_title_container)
        self.complete = False
        self.cantrip_url = "data/miracles/cantrips.json"

        self.non_magic_users = ["priest", "martyr", "monk", "virgin", "none"]
        self.db_cantrip = self.get_cantrips()
        self.db_lv1 = super().get_db("data/miracles/lv1.json")
        self.margin = 8
        self.display_spell = self.db_cantrip[0] 
        self.left_title = Title(self.display_spell["name"], self.left_title_container)
        self.spell_list = self.get_spell_list()
        self.check_box_list = CheckBoxList(
            self.right_page.move(0, self.right_title.rect.height),
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

    def get_spell_list(self):
        arr = []
        for value in self.db_cantrip:
            t = value["name"]
            if len(t) > 7:
                t = value["name"][:7] + "..."
            arr.append({"id": value["name"], "text": t, "value": value["name"]})
        return arr
        
    def render_text(self):
        self.left_title = Title(self.display_spell["name"], self.left_title_container)
        x = self.left_page.left + self.margin
        y = self.left_title_container.bottom + self.margin
        btn_con = pygame.Rect((self.left_page.left + self.left_page.width/2, y), (self.left_page.width/2, 32))
        self.accept_btn = Button('accept', 'accept', btn_con, 'accept')
        self.range = SmallTitle(
            f"Range: {self.display_spell["range"]}", 
            top_left=(x,y)
        )
        self.casting_time = Text(
            f"Casting Time: {self.display_spell["casting_time"]}", 
            has_underline=True, 
            top_left=(x, self.range.rect.bottom + self.margin)
        )
        self.duration = Text(
            f"Duration: {self.display_spell["duration"]}", 
            has_underline=True, 
            top_left=(x, self.casting_time.rect.bottom + self.margin)
        )
        con = pygame.Rect(
            (x, self.duration.rect.bottom + self.margin), 
            (self.left_page.width, self.left_page.height - y)    
        )
        self.desc_text_box = TextBox(self.display_spell["desc"], con)

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
        self.check_box_list.draw_list(screen)
        screen.blit(self.scroll_bar.image, self.scroll_bar.rect)
        screen.blit(self.range.image, self.range.rect)
        screen.blit(self.casting_time.image, self.casting_time.rect)
        screen.blit(self.duration.image, self.duration.rect)
        screen.blit(self.desc_text_box.image, self.desc_text_box.rect)
        self.accept_btn.blitme(screen)
