import pygame
from map import Map

class BattleMap(Map):
    def __init__(self):
        super().__init__()
        self.spacing_grid = self.get_spacing_grid()
        self.spacing_grid_rect = self.spacing_grid.get_rect()
    
    def get_spacing_grid(self):
        grid = pygame.Surface(
            (self.settings.screen_width, self.settings.screen_height), 
            pygame.SRCALPHA
        ).convert_alpha()
        vertical = pygame.Surface((1, self.size)).convert_alpha()
        vertical.fill((0,0,30))
        vertical.set_alpha(50)
        horizontal = pygame.Surface((self.size, 1)).convert_alpha()
        horizontal.fill((0,0,30))
        horizontal.set_alpha(50)
        x = 0
        y = 0
        while y < self.settings.screen_height:
            while x < self.settings.screen_width:
                grid.blit(vertical, (x, y))
                grid.blit(vertical, (x + self.size - 1, y))
                grid.blit(horizontal, (x, y))
                grid.blit(horizontal, (x, y + self.size - 1))
                x += self.size
            x = 0
            y += self.size
        return grid
    
    def blit_spacing_grid(self, screen):
        screen.blit(self.spacing_grid, self.spacing_grid_rect)

    # def blit_overlay(self, player_rect, screen):
    #     pass
    