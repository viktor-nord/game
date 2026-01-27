import pygame
import pygame.font
from pathlib import Path
import json

from page import Page
from font import PlainText, Title
from settings import Settings
from button import CheckBoxList

class AbilityPage(Page):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.player = self.get_player()
        self.left_title = Title("Proficiencies", self.left_title_container)
        proficiencies_path = Path("data/proficiencies.json")
        self.proficiencies_list = json.loads(proficiencies_path.read_text()) 
        self.complete = False
        self.selected_proficiencies = []
        self.proficiencies_list_container = self.left_page.copy()
        self.proficiencies_list_container.top = self.left_title_container.bottom + 8
        self.proficiencies_max_amount = self.player["pa"]
        self.proficiencies = CheckBoxList(
            game, 
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
        with open(self.db_url, "r") as db:
            player = json.load(db)
        if player["general"]["race"] == "" or player["religion"]["practice"] == "":
            return dic
        with open("data/rases.json", "r") as races_db:
            races = json.load(races_db)
            dic["abi"] = races[player["general"]["race"]]["abi"]
        with open("data/classes.json", "r") as practice_db:
            practice = json.load(practice_db)
            p = practice[player["religion"]["practice"]]
            dic["pa"] = p["proficiency_choices"]["choose"]
            dic["po"] = p["proficiency_choices"]["options"]
            dic["primary"] = p["primary_skill"]
        return dic

    def get_disabled_proficiencies(self, acceptable_proficiencies):
        l = []
        for pro in self.proficiencies_list:
            if pro not in acceptable_proficiencies:
                l.append(pro)
        return l

    def get_p_list(self):
        return [{"id": proficiencies, "text": proficiencies, "value": proficiencies} for proficiencies in self.proficiencies_list]

    def reset(self):
        self.player = self.get_player()
        self.selected_proficiencies = []
        self.proficiencies_max_amount = self.player["pa"]
        self.proficiencies = CheckBoxList(
            self.game, 
            self.proficiencies_list_container, 
            self.get_p_list(),
            slim = True,
            multi = True,
            amount = self.proficiencies_max_amount,
            disabled = self.get_disabled_proficiencies(self.player["po"])
        )
        self.abilities = self.populate_abilities()


    def get_info_text(self, selected):
        text = f"{selected} out of {self.proficiencies_max_amount} proficiencies"
        self.proficiencies_info = PlainText(text)
        self.proficiencies_info.rect.center = self.left_page.center
        self.proficiencies_info.rect.bottom = self.left_page.bottom
        
    def populate_abilities(self):
        self.player["abi"]
        abilities = []
        ac = self.right_page.copy() # ability container
        ac.height -= self.right_title_container.height + 8
        ac.top = self.right_title_container.bottom + 8
        w = ac.width // 2
        h = ac.height // 3
        for i, ability in enumerate(self.ability_list):
            bonus = 0
            for abi in self.player["abi"]:
                if abi["name"] == ability[:3]:
                    bonus = abi["val"]
            l = ac.left if i % 2 == 0 else ac.left + w
            t = ac.top 
            if i == 2 or i == 3:
                t += h
            if i > 3:
                t += h * 2
            container = pygame.Rect((l, t), (w,h))
            abilities.append(AbilityBox(ability[:3], container, bonus))
        return abilities

    def check_click(self):
        proficiencies_list = self.proficiencies.check_click()
        if proficiencies_list:
            self.selected_proficiencies = proficiencies_list
            self.get_info_text(len(self.selected_proficiencies))
        taken = set(a.value_index for a in self.abilities)
        for ability in self.abilities:
            operator = ability.handle_click()
            if operator:
                ability.change_value(operator, taken)
        self.check_if_complete()

    def check_if_complete(self):
        is_complete = True
        for a in self.abilities:
            if a.value_index == 0:
                is_complete = False
        if len(self.proficiencies.selected) < self.proficiencies_max_amount:
            is_complete = False
        self.complete = is_complete

    def update(self):
        self.proficiencies.update()

    def blitme(self, screen):
        super().blitme(screen)
        for ability in self.abilities:
            screen.blit(ability.image, ability.parent)
        screen.blit(self.left_title.image, self.left_title.rect)
        screen.blit(self.right_title.image, self.right_title.rect)
        self.proficiencies.draw_list(screen)
        screen.blit(self.proficiencies_info.text, self.proficiencies_info.rect)

class AbilityBox:
    def __init__(self, label, parent, bonus=0):
        self.value_index = 0
        self.test = label
        self.parent = parent
        self.bonus = bonus
        self.values = [0, 8, 10, 12, 13, 14, 15]
        url = "assets/ui_sprites/Sprites/Content/"
        self.image = pygame.Surface((parent.width, parent.height), pygame.SRCALPHA).convert_alpha()
        self.holder_image = pygame.image.load(url + "5 Holders/3.png").convert_alpha() # 80 x 80
        self.button_holer = pygame.image.load(url + "5 Holders/7.png").convert_alpha()
        self.minus_img = pygame.image.load(url + "2 Icons/2.png").convert_alpha()
        self.plus_img = pygame.image.load(url + "2 Icons/3.png").convert_alpha()
        self.bonus_image = pygame.image.load(url + "5 Holders/6.png").convert_alpha()
        self.bonus_text = PlainText(str(bonus), size=24)
        self.font = pygame.font.Font('assets/font/ThaleahFat.ttf', 22)
        self.big_font = pygame.font.Font('assets/font/ThaleahFat.ttf', 42)
        self.label = self.font.render(label, False, Settings().text_color)
        img_rect = self.image.get_rect()
        left_side = self.image.get_rect(width = self.image.get_width() - self.holder_image.get_width())
        self.minus_rect = self.button_holer.get_rect(centery = left_side.centery, right = left_side.width // 2)
        self.plus_rect = self.button_holer.get_rect(centery = left_side.centery, left = left_side.width // 2)
        self.label_container = self.label.get_rect(centerx = left_side.centerx, y = 16 + 8)
        self.image_holder_container = self.holder_image.get_rect(
            centery = img_rect.centery, right = img_rect.right-8
        )
        self.bonus_image_rect = self.bonus_image.get_rect(top=self.image_holder_container.top - 8, left = self.image_holder_container.left)
        self.blit_image()

    def blit_image(self):
        val = str(self.bonus) if self.bonus else "-"
        if self.values[self.value_index] != 0:
            val = str(self.values[self.value_index] + self.bonus)
        self.ability_text = self.big_font.render(val, False, Settings().text_color)
        self.image.blit(self.button_holer, (self.minus_rect))
        self.image.blit(self.button_holer, (self.plus_rect))
        self.image.blit(self.minus_img, (self.minus_img.get_rect(center = self.minus_rect.center)))
        self.image.blit(self.plus_img, (self.plus_img.get_rect(center = self.plus_rect.center)))
        self.image.blit(self.label, self.label_container)
        self.image.blit(self.holder_image, self.image_holder_container)
        self.image.blit(self.ability_text, self.ability_text.get_rect(center = self.image_holder_container.center))
        self.image.blit(self.bonus_image, self.bonus_image_rect)
        self.image.blit(self.bonus_text.text, self.bonus_text.text.get_rect(center = self.bonus_image_rect.center))

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        min = pygame.Rect((self.parent.x + self.minus_rect.x, self.parent.y + self.minus_rect.y), (self.minus_rect.width, self.minus_rect.height))
        plus = pygame.Rect((self.parent.x + self.plus_rect.x, self.parent.y + self.plus_rect.y), (self.plus_rect.width, self.plus_rect.height))
        if min.collidepoint(pos):
            return "-"
        if plus.collidepoint(pos):
            return "+"
        return None

    def change_value(self, operator, options):
        l = list(range(0, len(self.values)))
        if operator == "+":
            for i in l:
                if i > self.value_index and i not in options:
                    self.value_index = i
                    break
        else:
            l.reverse()
            if 0 in options:
                options.remove(0)
            for i in l:
                if i < self.value_index and i not in options:
                    self.value_index = i
                    break
        self.blit_image()
    
    def get_value(self):
        return self.values[self.value_index] + self.bonus