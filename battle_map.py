import pygame
from map import Map

class BattleMap(Map):
    def __init__(self, map_id='battle_1'):
        super().__init__(map_id)
        self.spacing_grid = self.get_spacing_grid()

    def get_spacing_grid(self, available_tiles=[], unavailable_tiles=[]):
        w, h = self.settings.screen_width, self.settings.screen_height
        grid = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        vertical_unavaliable = pygame.Surface((1, self.size)).convert_alpha()
        vertical_unavaliable.fill((255,0,0))
        vertical_unavaliable.set_alpha(100)
        horizontal_unavaliable = pygame.Surface((self.size, 1)).convert_alpha()
        horizontal_unavaliable.fill((255,0,0))
        horizontal_unavaliable.set_alpha(100)
        vertical_avaliable = pygame.Surface((1, self.size)).convert_alpha()
        vertical_avaliable.fill((0,0,255))
        vertical_avaliable.set_alpha(100)
        horizontal_avaliable = pygame.Surface((self.size, 1)).convert_alpha()
        horizontal_avaliable.fill((0,0,255))
        horizontal_avaliable.set_alpha(100)
        x = 0
        y = 0
        while y < self.settings.screen_height:
            while x < self.settings.screen_width:
                pos = [x // self.size, y // self.size]
                if pos in unavailable_tiles:
                    grid.blit(vertical_unavaliable, (x, y))
                    grid.blit(vertical_unavaliable, (x + self.size - 1, y))
                    grid.blit(horizontal_unavaliable, (x, y))
                    grid.blit(horizontal_unavaliable, (x, y + self.size - 1))
                if pos in available_tiles:
                    grid.blit(vertical_avaliable, (x, y))
                    grid.blit(vertical_avaliable, (x + self.size - 1, y))
                    grid.blit(horizontal_avaliable, (x, y))
                    grid.blit(horizontal_avaliable, (x, y + self.size - 1))
                x += self.size
            x = 0
            y += self.size
        return grid

    def update_grid(self, available_tiles, unavailable_tiles):
        self.spacing_grid = self.get_spacing_grid(available_tiles, unavailable_tiles)

    def blit_spacing_grid(self, screen):
        screen.blit(self.spacing_grid, (0,0))

    # def blit_overlay(self, player_rect, screen):
    #     pass
    