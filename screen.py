import pygame as py
from pytmx.util_pygame import load_pygame
from start_screen import StartScreen

class Screen:
    def __init__(self, game, settings):
        self.game = game
        self.settings = settings
        self.box = py.display.set_mode((
            self.settings.screen_width, 
            self.settings.screen_height
        ))
        self.screen_rect = self.box.get_rect()
        py.display.set_caption('Akavir: God of none')
        self.tmxdata = load_pygame('map/example_maptmx.tmx')
        self.start_screen = StartScreen(self)

    def update_screen(self):
        self.box.fill((100,100,100))
        self.blit_all_tiles()
        self.box.blit(
            self.game.player.image, 
            self.game.player.rect
        )
        if self.game.game_pause:
            self.start_screen.blitme()
        py.display.flip()

    def blit_all_tiles(self):
        for i, layer in enumerate(self.tmxdata):
            for tile in layer.tiles():
                x_pixel = tile[0] * self.settings.tile_size
                y_pixel = tile[1] * self.settings.tile_size
                img = py.transform.scale(tile[2], (self.settings.tile_size, self.settings.tile_size))
                self.screen.blit(img, (x_pixel, y_pixel))
