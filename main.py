import sys
import pygame
from pytmx.util_pygame import load_pygame

from player import Player
from settings import Settings

class Main():
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Akavir: God of none')
        self.tmxdata = load_pygame('map/example_maptmx.tmx')
        self.counter = 0
        self.game_is_running = True
        self.player = Player(self)

    def run(self):
        while self.game_is_running:
            self.check_event()
            self.player.update()
            self.clock.tick(60)
            self.update_screen()

    def update_screen(self):
        self.screen.fill((100,100,100))
        self.blit_all_tiles()
        self.screen.blit(self.player.image, self.player.rect)
        self.blit_all_overlay()
        pygame.display.flip()

    def blit_all_tiles(self):
        for layer in self.tmxdata:
            for tile in layer.tiles():
                x_pixel = tile[0] * self.settings.tile_size
                y_pixel = tile[1] * self.settings.tile_size
                img = pygame.transform.scale(tile[2], (self.settings.tile_size, self.settings.tile_size))
                self.screen.blit(img, (x_pixel, y_pixel))

    def blit_all_overlay(self):
        y_axe = self.player.rect.y // self.settings.tile_size
        x_axe = self.player.rect.x // self.settings.tile_size
        for i, layer in enumerate(self.tmxdata):
            if i > 0:
                for tile in layer.tiles():
                    if tile[1] * self.settings.tile_size > self.player.rect.y:
                        x_pixel = tile[0] * self.settings.tile_size
                        y_pixel = tile[1] * self.settings.tile_size
                        self.screen.blit(tile[2], (x_pixel, y_pixel))

    def check_event(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            self.player.moving_down = keys[pygame.K_DOWN]
            self.player.moving_up = keys[pygame.K_UP]
            self.player.moving_right = keys[pygame.K_RIGHT]
            self.player.moving_left = keys[pygame.K_LEFT]
            if event.type == pygame.QUIT:
                sys.exit()
            

if __name__ == '__main__':
    game = Main()
    game.run()
    pygame.quit()
