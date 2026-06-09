import pygame
import pygame.font
from page import Page
from font import PlainText, Title
from settings import Settings
from button import CheckBoxList

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
        dic["abi"] = races[player["general"]["race"]]["abi"]
        practice = self.get_db("data/classes.json")
        p = practice[player["religion"]["practice"]]
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

    def reset(self):
        self.player = self.get_player()
        # self.selected_proficiencies = []
        self.proficiencies_max_amount = self.player["pa"]
        s = self.proficiencies.selected
        self.proficiencies = CheckBoxList(
            self.proficiencies_list_container, 
            self.get_p_list(),
            slim = True,
            multi = True,
            amount = self.proficiencies_max_amount,
            disabled = self.get_disabled_proficiencies(self.player["po"])
        )
        self.proficiencies.selected = s
        vals = []
        for x in self.abilities:
            vals.append([x.label_text, x.value_index])
        self.abilities = self.populate_abilities()
        for val in vals:
            for i, a in enumerate(self.abilities):
                if val[0] == a.label_text:
                    self.abilities[i].value_index = val[1]

    def get_info_text(self, selected):
        text = f"{selected} out of {self.proficiencies_max_amount} proficiencies"
        self.proficiencies_info = PlainText(text)
        self.proficiencies_info.rect.center = self.left_page.center
        self.proficiencies_info.rect.bottom = self.left_page.bottom
        
    def populate_abilities(self):
        abilities = []
        a, b = self.right_page, self.right_title_container.height
        ac = pygame.Rect((a.x, a.y + b + 8), (a.width, a.height - b + 8))
        w, h = ac.width // 2, ac.height // 3
        for i, ability in enumerate(self.ability_list):
            bonus = 0
            for abi in self.player["abi"]:
                if abi["name"] == ability[:3]:
                    bonus = abi["val"]
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
        screen.blits([(ability.image, ability.parent) for ability in self.abilities])
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
        url = "assets/ui_sprites/Sprites/Content/"
        self.image = pygame.Surface((parent.width, parent.height), pygame.SRCALPHA).convert_alpha()
        self.bonus_text = PlainText(str(bonus), size=24)
        self.font = pygame.font.Font('assets/font/ThaleahFat.ttf', 22)
        self.big_font = pygame.font.Font('assets/font/ThaleahFat.ttf', 42)
        self.label = self.font.render(label, False, Settings().text_color)
        self.holder_image = img(url + "5 Holders/3.png")
        self.button_holer = img(url + "5 Holders/7.png")
        self.minus_img = img(url + "2 Icons/2.png")
        self.plus_img = img(url + "2 Icons/3.png")
        self.bonus_image = img(url + "5 Holders/6.png")
        img_rect = self.image.get_rect()
        left_side = self.image.get_rect(width = img_rect.width - self.holder_image.get_width())
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
        self.image.blit(self.button_holer, self.minus_rect)
        self.image.blit(self.button_holer, self.plus_rect)
        self.image.blit(self.minus_img, self.minus_img.get_rect(center = self.minus_rect.center))
        self.image.blit(self.plus_img, self.plus_img.get_rect(center = self.plus_rect.center))
        self.image.blit(self.label, self.label_container)
        self.image.blit(self.holder_image, self.image_holder_container)
        self.image.blit(self.ability_text, self.ability_text.get_rect(center = self.image_holder_container.center))
        self.image.blit(self.bonus_image, self.bonus_image_rect)
        self.image.blit(self.bonus_text.text, self.bonus_text.text.get_rect(center = self.bonus_image_rect.center))

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        pa, p, m = self.parent, self.plus_rect, self.minus_rect
        min = pygame.Rect((pa.x + m.x, pa.y + m.y), (m.width, m.height))
        plus = pygame.Rect((pa.x + p.x, pa.y + p.y), (p.width, p.height))
        if min.collidepoint(pos):
            return "-"
        if plus.collidepoint(pos):
            return "+"
        return None

    def change_value(self, operator, taken):
        l = [x for x in range(0, len(self.values))]
        if operator == "+":
            self.value_index = next(val for val in l if val > self.value_index and val not in taken)
        else:
            l.reverse()
            try:
                self.value_index = next(val for val in l if val < self.value_index and val not in taken)
            except StopIteration:
                self.value_index = 0
        self.blit_image()
    
    def get_value(self):
        return self.values[self.value_index] + self.bonus
    
def img(src):
    return pygame.image.load(src).convert_alpha()
