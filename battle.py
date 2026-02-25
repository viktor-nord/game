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
        self.battle_map = BattleMap()
        self.player = Player()
        self.npc_1 = Npc('jon', (1, 13))
        self.npc_2 = Npc('bob', (11, 11))
        self.npc_3 = Npc('mike', (11, 8))
        self.npc_group = [self.npc_1, self.npc_2, self.npc_3]
        # self.action_wheel = ActionWheel(self.player.rect)

    def update(self):
        self.battle_map.mobile_collision_grid = {}
        self.battle_map.mobile_collision_grid[self.player.id] = self.player.get_coordinates()
        for npc in self.npc_group:
            pos = npc.get_coordinates()
            self.battle_map.mobile_collision_grid[npc.id] = pos
        posible_moves = self.battle_map.check_collision(self.player)
        self.player.update(posible_moves)
        # self.action_wheel.update()

    def blitme(self, screen):
        self.battle_map.blit_all_tiles(screen)
        for npc in self.npc_group:
            npc.blitme(screen)
        self.player.blitme(screen)
        # self.battle_map.blit_overlay(self.player.rect, screen)
        self.battle_map.blit_spacing_grid(screen)
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
