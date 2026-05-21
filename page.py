import pygame
import json

from book import Book
from settings import Settings

class Page:
    def __init__(self):
        self.settings = Settings()
        self.player_url = "save/player.json"
        self.bg = pygame.image.load(
            'assets/ui_sprites/Sprites/Book Desk/3.png'
        ).convert_alpha()
        self.bg_rect = self.bg.get_rect(center = self.settings.center)
        self.book = Book()
        self.right_page = pygame.Rect((532, 64),(291, 360))
        self.left_page = pygame.Rect((202, 64),(291, 360))
        self.right_title_container = self.right_page.copy()
        self.right_title_container.height = 42
        self.left_title_container = self.left_page.move(16,0)
        self.left_title_container.height = 42

    def blitme(self, screen):
        screen.blit(self.bg, self.bg_rect)
        self.book.blitme(screen)

    def get_db(self, path):
        with open(path, "r") as db:
            return json.load(db)