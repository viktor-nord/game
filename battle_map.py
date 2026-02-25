import pygame
from map import Map

class BattleMap(Map):
    def __init__(self):
        super().__init__('battle_1')
        self.spacing_grid = self.get_spacing_grid()

    def get_spacing_grid(self, available_tiles=[]):
        grid = pygame.Surface(
            (self.settings.screen_width, self.settings.screen_height), 
            pygame.SRCALPHA
        ).convert_alpha()
        vertical = pygame.Surface((1, self.size)).convert_alpha()
        vertical.fill((0,0,0))
        vertical.set_alpha(100)
        horizontal = pygame.Surface((self.size, 1)).convert_alpha()
        horizontal.fill((0,0,0))
        horizontal.set_alpha(100)

        vertical_avaliable = pygame.Surface((1, self.size)).convert_alpha()
        vertical_avaliable.fill((0,0,255))
        horizontal_avaliable = pygame.Surface((self.size, 1)).convert_alpha()
        horizontal_avaliable.fill((0,0,255))

        x = 0
        y = 0
        while y < self.settings.screen_height:
            while x < self.settings.screen_width:
                if [x // self.size, y // self.size] in available_tiles:
                    grid.blit(vertical_avaliable, (x, y))
                    grid.blit(vertical_avaliable, (x + self.size - 1, y))
                    grid.blit(horizontal_avaliable, (x, y))
                    grid.blit(horizontal_avaliable, (x, y + self.size - 1))
                else:
                    grid.blit(vertical, (x, y))
                    grid.blit(vertical, (x + self.size - 1, y))
                    grid.blit(horizontal, (x, y))
                    grid.blit(horizontal, (x, y + self.size - 1))
                x += self.size
            x = 0
            y += self.size
        return grid

    def update_grid(self, available_tiles):
        self.spacing_grid = self.get_spacing_grid(available_tiles)

    def blit_spacing_grid(self, screen):
        screen.blit(self.spacing_grid, (0,0))

    # def blit_overlay(self, player_rect, screen):
    #     pass
    