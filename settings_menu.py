import pygame

from settings import Settings
from book import Book
from button import AltButton


class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.settings = Settings()
        self.open = False
        self.holder = pygame.image.load('assets/ui_sprites/Sprites/Content/5 Holders/6.png').convert_alpha()
        self.holder_rect = self.holder.get_rect(top = 8, right = self.settings.screen_width - 8)
        self.gear_img = pygame.image.load('assets/ui_sprites/node_2D/icon_gear.png').convert_alpha()
        self.gear_rect = self.gear_img.get_rect(center = self.holder_rect.center)
        self.bg = Book()
        self.right_page = pygame.Rect((532, 64),(291, 360))
        self.left_page = pygame.Rect((202, 64),(291, 360))
        self.btn = AltButton(555, 'shit', pygame.Rect((600, 200), (100, 100)), 555)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.open:
                if self.btn.rect.collidepoint(pos):
                    self.game.mode = 'start_screen'
                # change this shit
                self.open = False
            else:
                self.open = self.holder_rect.collidepoint(pos)

    def blitme(self, screen):
        if self.open:
            self.bg.blitme(screen)
            self.btn.blitme(screen)
        else:
            screen.blit(self.holder, self.holder_rect)
            screen.blit(self.gear_img, self.gear_rect)