import sys
import pygame

from player import Player
from settings import Settings
from npc import Npc
from battle_map import BattleMap
from action_wheel import ActionWheel

class Battle():
    def __init__(self):
        self.game_pause = False
        self.settings = Settings()
        self.map = BattleMap()
        self.player = Player([5, 10])
        self.npc_1 = Npc('jon', (6, 3))
        self.npc_2 = Npc('bob', (24, 3))
        self.npc_3 = Npc('mike', (5, 11))
        self.npc_group = [self.npc_1, self.npc_2, self.npc_3]
        for npc in self.npc_group:
            pos = npc.get_coordinates()
            self.map.mobile_collision_grid[npc.id] = pos
        self.available_tiles = [] 
        self.unavailable_tiles = []
        self.get_available_tiles()
        self.map.update_grid(self.available_tiles, self.unavailable_tiles)
        # self.action_wheel = ActionWheel(self.player.rect)
    
    def get_available_tiles(self):
        x = self.player.rect.x // self.settings.tile_size
        y = self.player.rect.y // self.settings.tile_size
        dirs = [
            [x - 1, y],
            [x + 1, y],
            [x, y - 1],
            [x, y + 1],
        ]
        for pos in dirs:
            collision = self.map.get_tile_collision(pos[0], pos[1])
            if collision == None:
                self.available_tiles.append([pos[0], pos[1]])
            else:
                self.unavailable_tiles.append([pos[0], pos[1]])

    def update(self):
        self.map.mobile_collision_grid = {}
        self.map.mobile_collision_grid[self.player.id] = self.player.get_coordinates()
        for npc in self.npc_group:
            pos = npc.get_coordinates()
            self.map.mobile_collision_grid[npc.id] = pos
        posible_moves = self.map.check_collision(self.player)
        self.player.update(posible_moves)
        # self.action_wheel.update()

    def blitme(self, screen):
        self.map.blit_all_tiles(screen)
        for npc in self.npc_group:
            npc.blitme(screen)
        self.player.blitme(screen)
        # self.map.blit_overlay(self.player.rect, screen)
        self.map.blit_spacing_grid(screen)
        # self.action_wheel.blitme(screen)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            pass # scroll_down = True if event.y < 0 else False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click()
        elif event.type == pygame.KEYDOWN:
            self.handle_key(event.key, True)
        elif event.type == pygame.KEYUP:
            self.handle_key(event.key, False)

    def handle_key(self, key, is_down):
        if key == pygame.K_SPACE:
            if is_down:
                self.handle_action()
        elif key == pygame.K_p:
            self.game_pause = True
        else:
            self.player.handle_movement(key, is_down)        

    def handle_action(self):
        pass

    def handle_click(self):
        pass
        # self.action_wheel.handle_click()
