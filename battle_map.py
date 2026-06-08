import pygame
import copy
from map import Map

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
        char = copy.copy(battle_object[current_id])
        if char.steps_amount < 1:
            return
        char.speed = 32
        self.available_tiles = []
        self.unavailable_tiles = []
        posible_moves = self.check_collision(char)
        r, m = char.get_coordinates(), char.movement
        for key, val in posible_moves.items():
            pos = [r[0] + m[key][0], r[1] + m[key][1]]
            if val:
                self.available_tiles.append(pos)
            else:
                self.unavailable_tiles.append(pos)

    def get_grid_surf(self, color):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA).convert_alpha()
        for line in [(0, 0, True), (0, 0, False), (0, self.size-1, True), (self.size-1, 0, False)]:
            wh = (self.size, 1) if line[2] else (1, self.size)
            l = pygame.Surface(wh).convert()
            l.fill(color)
            surf.blit(l, (line[0], line[1]))
        return surf

    def get_spacing_grid(self, available_tiles=[], unavailable_tiles=[]):
        w, h = self.settings.screen_width, self.settings.screen_height
        grid = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        available = self.get_grid_surf(pygame.Color(0,0,255,100))
        unavailable = self.get_grid_surf(pygame.Color(255,0,0,100))
        for tile_a in self.available_tiles:
            grid.blit(available, (tile_a[0] * self.size, tile_a[1] * self.size))
        for tile_u in self.unavailable_tiles:
            grid.blit(unavailable, (tile_u[0] * self.size, tile_u[1] * self.size))
        return grid

    def update_grid(self, available_tiles, unavailable_tiles):
        self.spacing_grid = self.get_spacing_grid(available_tiles, unavailable_tiles)

    def blit_spacing_grid(self, screen):
        screen.blit(self.spacing_grid, (0,0))

    # def blit_overlay(self, player_rect, screen):
    #     pass
    