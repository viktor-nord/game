import pygame

from button import CheckBoxList
from font import Text, Title
from book import Book
from text_box import TextBox

class CharacterCreation:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.bg = pygame.image.load('assets/ui_sprites/Sprites/Book Desk/3.png')
        self.bg_rect = self.bg.get_rect(center = game.screen_rect.center)
        self.book = Book(game)
        self.right_page = pygame.Rect((533, 64),(288, 360))
        self.left_page = pygame.Rect((203, 64),(288, 360))
        self.right_title_container = self.right_page.copy()
        self.right_title_container.height = 42
        self.right_title = Title("Faith", self.right_title_container)
        self.check_box_container = self.right_page.copy()
        margin = self.right_title.rect.height + 16
        self.check_box_container.y += margin
        self.check_box_container.height -= margin
        self.buttons = CheckBoxList(
            self.game, 
            self.check_box_container,
            [
                {"id":"munk", "text":"Munk"},
                {"id":"cleric", "text":"Cleric"},
                {"id":"priest", "text":"Priest"},
            ] 
        )
        self.text_box_container = self.left_page.copy()
        self.text_box_container.height = 100
        self.text_box_container.y += 50
        self.text_box = TextBox(self.game, "this is a test text for the purpus of checking the lenght and height of the text box. now i m making the text box bigger", self.text_box_container)

    def update(self):
        self.buttons.update()
        self.text_box.update()

    def blitme(self):
        self.screen.blit(self.bg, self.bg_rect)
        self.book.blitme(self.screen)
        self.screen.blit(self.right_title.text, self.right_title.rect)
        self.buttons.draw_list()
        self.text_box.blitme()
        # pygame.draw.rect(self.screen, "red", self.right_page)
        # pygame.draw.rect(self.screen, "red", self.left_page)

    def handle_click(self):
        self.buttons.check_click()