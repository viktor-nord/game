import pygame
from map import Map
from utils import get_adjasent_cord

class BattleMap(Map):
    def __init__(self, map_id='battle_1'):
        super().__init__(map_id)
        self.available_tiles = []
        self.unavailable_tiles = []
        self.spacing_grid = self.get_spacing_grid()

    def load_grid_data(self, battle_object, current_id):
        for key, val in battle_object.items():
            pos = val.get_coordinates()
            self.mobile_collision_grid[key] = pos
        self.get_tile_availability(battle_object, current_id)
        self.update_grid(self.available_tiles, self.unavailable_tiles)

    def get_tile_availability(self, battle_object, current_id):
        c = battle_object[current_id]
        self.available_tiles = []
        self.unavailable_tiles = []
        pos = [c.rect.x // self.settings.tile_size, c.rect.y // self.settings.tile_size]
        dirs = get_adjasent_cord(pos)
        if c.steps_amount:
            for pos in dirs.values():
                collision_id = self.get_tile_collision(pos)
                if collision_id == None or collision_id == current_id:
                    self.available_tiles.append([pos[0], pos[1]])
                else:
                    self.unavailable_tiles.append([pos[0], pos[1]])

    def get_grid_surf(self, color, is_vertical):
        s = (1, self.size) if is_vertical else (self.size, 1)
        surf = pygame.Surface(s).convert_alpha()
        surf.fill(color)
        surf.set_alpha(100)
        return surf

    def get_spacing_grid(self, available_tiles=[], unavailable_tiles=[]):
        w, h = self.settings.screen_width, self.settings.screen_height
        grid = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        vertical_unavaliable = self.get_grid_surf((255,0,0), True)
        horizontal_unavaliable = self.get_grid_surf((255,0,0), False)
        vertical_avaliable = self.get_grid_surf((0,0,255), True)
        horizontal_avaliable = self.get_grid_surf((0,0,255), False)
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
    