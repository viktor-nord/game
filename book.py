import pygame as py

class Book:
    def __init__(self, game):
        self.game = game
        url = 'assets/ui_sprites/Sprites/Content Appear Animation/10 book/Frame 15_small.png'
        self.img = py.image.load(url).convert_alpha()
        self.book = py.transform.scale(
            self.img, (self.img.get_width() // 2, self.img.get_height() // 2)
        )
        self.book.set_colorkey((255,0,0))
        self.book.convert_alpha()
        self.rect = self.book.get_rect(center=game.screen_rect.center)

    def blitme(self, screen):
        screen.blit(self.book, self.rect)