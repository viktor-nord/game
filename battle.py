import sys
import pygame

from player import Player
from settings import Settings
from npc import Npc
from battle_map import BattleMap
from action_wheel import ActionWheel
from battle_ui import BattleUI

class Battle():
    def __init__(self):
        self.game_pause = False
        self.walking_animation = False
        self.settings = Settings()
        self.map = BattleMap()
        self.player = Player([5, 10])
        self.npc_1 = Npc('jon', (6, 3))
        self.npc_2 = Npc('bob', (24, 3))
        self.npc_3 = Npc('mike', (5, 11))
        self.ui = BattleUI()
        self.npc_group = [self.npc_1, self.npc_2, self.npc_3]
        self.player_moves_amount = self.player.data.speed // 10
        for npc in self.npc_group:
            pos = npc.get_coordinates()
            self.map.mobile_collision_grid[npc.id] = pos
        self.available_tiles = [] 
        self.unavailable_tiles = []
        self.get_tile_availability()
        self.map.update_grid(self.available_tiles, self.unavailable_tiles)
        player_rect_copy = self.player.rect.copy()
        player_rect_copy.x = 80
        player_rect_copy.y = 80
        self.action_wheel = ActionWheel(player_rect_copy)
    
    def get_tile_availability(self):
        self.available_tiles = []
        self.unavailable_tiles = []
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
        if self.walking_animation:
            self.check_walking_animation()
        self.player.update()
        self.action_wheel.update()

    def check_walking_animation(self):
        pos = [
            self.player.rect.x / self.settings.tile_size, 
            self.player.rect.y / self.settings.tile_size
        ]
        if pos[0] == float(self.player.moving_to[0]) and pos[1] == float(self.player.moving_to[1]):
            self.player.reset_movement()
            self.player_moves_amount -= 1
            self.walking_animation = False
            self.get_tile_availability()
            self.map.update_grid(self.available_tiles, self.unavailable_tiles)


    def blitme(self, screen):
        self.map.blit_all_tiles(screen)
        for npc in self.npc_group:
            npc.blitme(screen)
        self.player.blitme(screen)
        self.map.blit_spacing_grid(screen)
        self.ui.blitme(screen)
        if self.player_moves_amount > 0:
            circle_radius = self.player_moves_amount * self.settings.tile_size + self.player.rect.width // 2
            pygame.draw.circle(screen, (0,0,255), self.player.rect.center, circle_radius, width=2)
        self.action_wheel.blitme(screen)

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
        elif key == pygame.K_RIGHT or key == pygame.K_LEFT or key == pygame.K_UP or key == pygame.K_DOWN:
            self.handle_movement(key, is_down)

    def handle_movement(self, key, is_down):
        if is_down or self.player_moves_amount < 1:
            return
        x = self.player.rect.x // self.settings.tile_size
        y = self.player.rect.y // self.settings.tile_size
        is_moving = False
        if key == pygame.K_RIGHT:
            if [x + 1, y] in self.available_tiles:
                x += 1
                is_moving = True
        elif key == pygame.K_LEFT:
            if [x - 1, y] in self.available_tiles:
                x -= 1
                is_moving = True
        elif key == pygame.K_DOWN:
            if [x, y + 1] in self.available_tiles:
                y += 1
                is_moving = True
        elif key == pygame.K_UP:
            if [x, y - 1] in self.available_tiles:
                y -= 1
                is_moving = True
        if self.walking_animation == False and is_moving:
            self.walking_animation = True
            self.player.moving_to = [x, y]
            self.player.handle_movement(key, True)

    def handle_action(self):
        pass

    def handle_click(self):
        action = self.action_wheel.handle_click()
