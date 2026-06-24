import pygame
from page import Page
from font import PlainText, Text, Title
from settings import Settings
from button import CheckBoxList
from image import Image

class AbilityPage(Page):
    def __init__(self):
        super().__init__()
        self.player = self.get_player()
        self.left_title = Title("Proficiencies", self.left_title_container)
        self.proficiencies_list = super().get_db("data/proficiencies.json")
        self.complete = False
        self.selected_proficiencies = []
        self.proficiencies_list_container = self.left_page.move(0, self.left_title_container.height + 8)
        self.proficiencies_max_amount = self.player["pa"]
        self.proficiencies = CheckBoxList(
            self.proficiencies_list_container, 
            self.get_p_list(),
            slim = True,
            multi = True,
            amount = self.proficiencies_max_amount,
            disabled = self.get_disabled_proficiencies(self.player["po"])
        )
        self.ability_list = ["strength", "wisdom", "constitution", "dexterity", "intelligence", "charisma"]
        self.values = [0, 8, 10, 12, 13, 14, 15]
        self.abilities = self.populate_abilities()
        self.right_title = Title("Ability", self.right_title_container)
        self.get_info_text(0)

    def get_player(self):
        dic = {
            "abi": [],
            "pa": 1,
            "po": [],
            "primary": ""
        }
        player = self.get_db("save/player.json")
        if player["general"]["race"] == "" or player["religion"]["practice"] == "":
            return dic
        races = self.get_db("data/rases.json")
        practice = self.get_db("data/classes.json")
        p = practice[player["religion"]["practice"]]
        dic["abi"] = races[player["general"]["race"]]["abi"]
        dic["pa"] = p["proficiency_choices"]["choose"]
        dic["po"] = p["proficiency_choices"]["options"]
        dic["primary"] = p["primary_skill"]
        return dic

    def get_disabled_proficiencies(self, acceptable_proficiencies):
        l = self.proficiencies_list[:]
        for p in acceptable_proficiencies:
            l.remove(p)
        return l

    def get_p_list(self):
        return [{"id": p, "text": p, "value": p} for p in self.proficiencies_list]

    def get_info_text(self, selected):
        text = f"{selected} out of {self.proficiencies_max_amount} proficiencies"
        self.proficiencies_info = Text(text, parent=self.left_page)
        self.proficiencies_info.rect.bottom = self.left_page.bottom
        
    def populate_abilities(self):
        abilities = []
        a, b = self.right_page, self.right_title_container.height
        ac = pygame.Rect((a.x, a.y + b + 8), (a.width, a.height - b + 8))
        w, h = ac.width // 2, ac.height // 3
        for i, ability in enumerate(self.ability_list):
            bonus = next((abi["val"] for abi in self.player["abi"] if abi["name"] == ability[:3]), 0)
            l = ac.left if i % 2 == 0 else ac.left + w
            t = ac.top + i // 2 * h
            container = pygame.Rect((l, t), (w,h))
            abilities.append(AbilityBox(ability[:3], container, bonus))
        return abilities

    def check_click(self):
        self.selected_proficiencies = self.proficiencies.check_click()
        self.get_info_text(len(self.selected_proficiencies))
        taken = set(a.value_index for a in self.abilities)
        for ability in self.abilities:
            operator = ability.handle_click()
            if operator:
                ability.change_value(operator, taken)
        self.check_if_complete()

    def check_if_complete(self):
        abilities_check = all(x.value_index > 0 for x in self.abilities)
        prof_check = len(self.proficiencies.selected) < self.proficiencies_max_amount
        self.complete = abilities_check and not prof_check

    def update(self):
        self.proficiencies.update()

    def blitme(self, screen):
        super().blitme(screen)
        screen.blits([(ability.surf, ability.parent) for ability in self.abilities])
        screen.blit(self.left_title.image, self.left_title.rect)
        screen.blit(self.right_title.image, self.right_title.rect)
        self.proficiencies.draw_list(screen)
        screen.blit(self.proficiencies_info.text, self.proficiencies_info.rect)

class AbilityBox:
    def __init__(self, label, parent, bonus=0):
        self.value_index = 0
        self.label_text = label
        self.parent = parent
        self.bonus = bonus
        self.values = [0, 8, 10, 12, 13, 14, 15]
        self.surf = pygame.Surface((parent.width, parent.height), pygame.SRCALPHA).convert_alpha()
        self.get_content()
        self.get_rects()
        self.get_text(label)
        self.render_text()
        self.blit_image()

    def get_content(self):
        url = "assets/ui_sprites/Sprites/Content/"
        self.holder_image = Image(url + "5 Holders/3.png").image
        self.button_holer = Image(url + "5 Holders/7.png").image
        self.minus_img = Image(url + "2 Icons/2.png").image
        self.plus_img = Image(url + "2 Icons/3.png").image
        self.bonus_image = Image(url + "5 Holders/6.png").image

    def get_rects(self):
        img_rect = self.surf.get_rect()
        self.left_side = self.surf.get_rect(width = img_rect.width - self.holder_image.get_width())
        self.minus_rect = self.button_holer.get_rect(centery = self.left_side.centery, right = self.left_side.width // 2)
        self.plus_rect = self.minus_rect.move(self.minus_rect.width + 1, 0)
        self.image_holder_container = self.holder_image.get_rect(
            centery = img_rect.centery, right = img_rect.right-8
        )
        self.bonus_image_rect = self.bonus_image.get_rect(
            top = self.image_holder_container.top - 8, left = self.image_holder_container.left
        )

    def get_text(self, label):
        self.bonus_text = Text(str(self.bonus), size=24, parent=self.bonus_image_rect)
        self.label = Text(
            label, 
            size=22, 
            font_family='assets/font/ThaleahFat.ttf', 
            parent=self.left_side
        )
        self.label.rect.y = 24

    def render_text(self):
        val = self.values[self.value_index]
        text = str(val + self.bonus) if val != 0 else '-'
        self.ability_text = Text(text, size=42, font_family='assets/font/ThaleahFat.ttf', parent=self.image_holder_container)

    def blit_image(self):
        self.surf.blit(self.button_holer, self.minus_rect)
        self.surf.blit(self.button_holer, self.plus_rect)
        self.surf.blit(self.minus_img, self.minus_rect)
        self.surf.blit(self.plus_img, self.plus_rect)
        self.surf.blit(self.label.text, self.label.rect)
        self.surf.blit(self.holder_image, self.image_holder_container)
        self.surf.blit(self.bonus_image, self.bonus_image_rect)
        self.surf.blit(self.ability_text.text, self.ability_text.rect)
        self.surf.blit(self.bonus_text.text, self.bonus_text.rect)

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        min = self.minus_rect.move(self.parent.x, self.parent.y)
        plus = self.plus_rect.move(self.parent.x, self.parent.y)
        if min.collidepoint(pos):
            return "-"
        elif plus.collidepoint(pos):
            return "+"
        else:
            return None

    def change_value(self, operator, taken):
        l = [x for x in range(0, len(self.values))]
        if operator == "+":
            self.value_index = next((val for val in l if val > self.value_index and val not in taken), self.value_index)
        else:
            l.reverse()
            self.value_index = next((val for val in l if val < self.value_index and val not in taken), 0)
        self.render_text()
        self.blit_image()
    
    def get_value(self):
        return self.values[self.value_index] + self.bonus
