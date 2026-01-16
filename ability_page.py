from turtle import right, width
from matplotlib.style import available
import pygame
import pygame.font

from page import Page
from font import Title
from settings import Settings

class AbilityPage(Page):
    def __init__(self, game):
        super().__init__(game)
        self.ability_list = ["strength", "wisdom", "constitution", "dexterity", "intelligence", "charisma"]
        self.values = [8, 10, 12, 13, 14, 15]
        ac = self.right_page.copy() # ability container
        ac.height -= self.right_title_container.height + 8
        ac.top = self.right_title_container.bottom + 8
        w = ac.width // 2
        h = ac.height // 3
        self.abilities = []
        for i, ability in enumerate(self.ability_list):
            l = ac.left if i % 2 == 0 else ac.left + w
            t = ac.top 
            if i > 1 and i < 4:
                t += h
            if i > 3:
                t += h * 2
            con = pygame.Rect((l, t), (w,h))
            self.abilities.append([con, AbilityBox(ability[:3], con)])
        self.right_title = Title("Ability", self.right_title_container)

    def check_click(self):
        for ability in self.abilities:
            val = ability[1].handle_click()
            if val:
                ability[1].change_value(val)

    def update(self):
        pass
        # self.check_box_list.update()

    def blitme(self, screen):
        super().blitme(screen)
        for ability in self.abilities:
            screen.blit(ability[1].image, ability[0])
        screen.blit(self.right_title.image, self.right_title.rect)

class AbilityBox:
    def __init__(self, label, parent):
        self.value = 0
        self.test = label
        self.parent = parent
        url = "assets/ui_sprites/Sprites/Content/"
        self.image = pygame.Surface((parent.width, parent.height), pygame.SRCALPHA).convert_alpha()
        self.holder_image = pygame.image.load(url + "5 Holders/3.png").convert_alpha() # 80 x 80
        self.button_holer = pygame.image.load(url + "5 Holders/7.png").convert_alpha()
        self.minus_img = pygame.image.load(url + "2 Icons/2.png").convert_alpha()
        self.plus_img = pygame.image.load(url + "2 Icons/3.png").convert_alpha()
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
        self.blit_image()

    def blit_image(self):
        val = "-"
        if self.value != 0:
            val = str(self.value)
        self.ability_text = self.big_font.render(val, False, Settings().text_color)
        self.image.blit(self.button_holer, (self.minus_rect))
        self.image.blit(self.button_holer, (self.plus_rect))
        self.image.blit(self.minus_img, (self.minus_img.get_rect(center = self.minus_rect.center)))
        self.image.blit(self.plus_img, (self.plus_img.get_rect(center = self.plus_rect.center)))
        self.image.blit(self.label, self.label_container)
        self.image.blit(self.holder_image, self.image_holder_container)
        self.image.blit(self.ability_text, self.ability_text.get_rect(center = self.image_holder_container.center))

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        min = pygame.Rect((self.parent.x + self.minus_rect.x, self.parent.y + self.minus_rect.y), (self.minus_rect.width, self.minus_rect.height))
        plus = pygame.Rect((self.parent.x + self.plus_rect.x, self.parent.y + self.plus_rect.y), (self.plus_rect.width, self.plus_rect.height))
        if min.collidepoint(pos):
            return "-"
        if plus.collidepoint(pos):
            return "+"
        return None

    def change_value(self, val):
        if val == "+":
            self.value += 1
        else:
            if self.value > 0:
                self.value -= 1
        self.blit_image()