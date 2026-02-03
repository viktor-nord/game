import pygame
from pathlib import Path
import json

from book import Book

class Page:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.bg = pygame.image.load(
            'assets/ui_sprites/Sprites/Book Desk/3.png'
        ).convert_alpha()
        self.bg_rect = self.bg.get_rect(center = game.screen_rect.center)
        self.book = Book(game)
        self.right_page = pygame.Rect((532, 64),(291, 360))
        self.left_page = pygame.Rect((202, 64),(291, 360))
        self.right_title_container = self.right_page.copy()
        self.right_title_container.height = 42
        self.left_title_container = self.left_page.copy()
        self.left_title_container.height = 42

    def blitme(self, screen):
        screen.blit(self.bg, self.bg_rect)
        self.book.blitme(screen)

    def get_db(self, path):
        with open(path, "r") as db:
            return json.load(db)