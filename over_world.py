import sys
import pygame

from player import Player
from settings import Settings
from map import Map
from npc import Npc
from dialogs import Dialog

class OverWorld():
    def __init__(self, game):
        self.game = game
        self.game_pause = False
        self.start_battle = False
        self.settings = Settings()
        self.map = Map()
        self.player = Player(self)
        self.npc_1 = Npc(self, 'jon', self.map, (1, 13), movement_pattern='random')
        self.npc_2 = Npc(self, 'bob', self.map, (11, 11), movement_pattern=['right', 'down', 'up', 'left'])
        self.npc_3 = Npc(self, 'mike', self.map, (11, 8))
        self.npc_group = [self.npc_1, self.npc_2, self.npc_3]

    def update(self):
        self.map.mobile_collision_grid = {}
        self.map.mobile_collision_grid[self.player.id] = self.player.get_coordinates()
        for npc in self.npc_group:
            pos = npc.get_coordinates()
            self.map.mobile_collision_grid[npc.id] = pos
        self.player.update()
        for npc in self.npc_group:
            npc.check_movement()
            npc.update()

    def blitme(self, screen):
        self.map.blit_all_tiles(screen)
        for npc in self.npc_group:
            npc.blitme(screen)
            # screen.blit(npc.image, npc.rect)
        # screen.blit(self.player.image, self.player.rect)
        self.player.blitme(screen)
        self.map.blit_overlay(self.player.rect, screen)

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
            self.handle_player_movement(key, is_down)

    def handle_player_movement(self, key, is_down):
        not_colliding = self.map.check_collision(self.player.rect)
        if not_colliding:
            self.player.handle_movement(key, is_down)

    def handle_action(self):
        x, y = self.player.get_coordinates()
        dir = self.player.dir
        npc = None
        if dir == 'right':
            x += 1
        elif dir == 'left':
            x -= 1
        elif dir == 'down':
            y += 1
        elif dir == 'up':
            y -= 1
        for npc_id, pos in self.map.mobile_collision_grid.items():
            if x == pos[0] and y == pos[1]:
                npc = npc_id
        if npc == None:
            return
        if npc == 'mike':
            self.start_battle = True
        else:
            text = Dialog(npc)
            print(text.text)

    def handle_click(self):
        pass
