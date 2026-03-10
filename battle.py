import sys
import pygame
from random import randrange

from player import Player
from settings import Settings
from npc import Npc
from ally import Ally
from battle_map import BattleMap
from action_wheel import ActionWheel
from battle_ui import BattleUI

class Battle():
    def __init__(self):
        self.game_pause = False
        self.walking_animation = False
        self.allow_events = True
        self.turn_order = []
        self.current_id = 'player'
        self.settings = Settings()
        self.map = BattleMap()
        self.player = Player([5, 10])
        self.battle_object = {
            f"{self.player.id}": self.player, 
            "buddy": Ally(id='buddy', pos=(6, 11)),
            "jon": Npc('jon', (6, 3)), 
            "bob": Npc('bob', (24, 3), type='skeleton'), 
            "mike": Npc('mike', (5, 11)), 
        }
        self.ui = BattleUI(self.battle_object)
        self.available_tiles = [] 
        self.unavailable_tiles = []
        self.load_grid_data()
        self.action_wheel_target = None
        self.action_wheel = ActionWheel()
        self.init_battle() # call from parent instead

    def get_ui(self):
        dic = {}
        for id in self.turn_order:
            dic[f"{id}"] = self.battle_object[f"{id}"]
        self.ui = BattleUI(dic, self.current_id)

    def init_battle(self):
        self.roll_inisiative()
        self.get_ui()

    def load_grid_data(self):
        for key, val in self.battle_object.items():
            pos = val.get_coordinates()
            self.map.mobile_collision_grid[key] = pos
        self.get_tile_availability()
        self.map.update_grid(self.available_tiles, self.unavailable_tiles)

    def roll_inisiative(self):
        for id in self.battle_object.keys():
            self.turn_order.append(id)
        # dic = {}
        # for id in self.battle_object.keys():
        #     dic[id] = randrange(1,21)
        # self.turn_order = [k for k, v in sorted(dic.items(), key=lambda item: item[1])]
        self.current_id = self.turn_order[0]

    def get_tile_availability(self):
        self.available_tiles = []
        self.unavailable_tiles = []
        x = self.battle_object[self.current_id].rect.x // self.settings.tile_size
        y = self.battle_object[self.current_id].rect.y // self.settings.tile_size
        dirs = [
            [x - 1, y],
            [x + 1, y],
            [x, y - 1],
            [x, y + 1],
        ]
        if self.battle_object[self.current_id].steps_amount:
            for pos in dirs:
                collision = self.map.get_tile_collision(self.current_id, pos[0], pos[1])
                if collision == None:
                    self.available_tiles.append([pos[0], pos[1]])
                else:
                    self.unavailable_tiles.append([pos[0], pos[1]])

    def handle_turn(self):
        c = self.battle_object[self.current_id]
        if c.is_party_member:
            self.allow_events = True
        else:
            if c.steps_amount < 1:
                self.end_turn()
            else:
                self.battle_object[self.current_id].battle_ai()
                self.walking_animation = True

    def update(self):
        if self.walking_animation:
            self.check_walking_animation()
        else:
            self.handle_turn()
        for char in self.battle_object.values():
            char.update()
        # self.battle_object[self.current_id].update()
        if self.action_wheel_target:
            self.action_wheel.update()

    def check_walking_animation(self):
        c = self.battle_object[self.current_id]
        pos = [
            c.rect.x / self.settings.tile_size,
            c.rect.y / self.settings.tile_size
        ]
        if pos[0] == float(c.moving_to[0]) and pos[1] == float(c.moving_to[1]):
            self.battle_object[self.current_id].reset_movement()
            self.battle_object[self.current_id].steps_amount -= 1
            self.get_ui()
            self.walking_animation = False
            self.load_grid_data()

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
        elif key == pygame.K_p and is_down:
            self.game_pause = True
        elif key == pygame.K_q and is_down:
            self.end_turn()
        elif key == pygame.K_RIGHT or key == pygame.K_LEFT or key == pygame.K_UP or key == pygame.K_DOWN:
            self.handle_movement(key, is_down)

    def handle_movement(self, key, is_down):
        # self.load_grid_data()
        c = self.battle_object[self.current_id]
        if is_down or c.steps_amount < 1:
            return
        x = c.rect.x // self.settings.tile_size
        y = c.rect.y // self.settings.tile_size
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
            self.battle_object[self.current_id].moving_to = [x, y]
            self.battle_object[self.current_id].handle_movement(key, True)

    def handle_action(self):
        pass

    def melee_attack(self, id):
        self.current_id # person attacking
        for key, val in self.battle_object.items():
            if key == id:
                val.take_damage(1, 'bludgeoning')
                print(f"{self.current_id} is attacking {key}")

    def handle_action_wheel(self, action_obj):
        if action_obj['val'] == 'primary':
            if self.battle_object[self.current_id].actions_amount < 1:
                print('You have already used your action')
                return
            if self.check_if_next_to():
                self.melee_attack(action_obj['id'])
                self.battle_object[self.current_id].actions_amount -= 1
                self.get_ui()
            else:
                print("you are to far away")

    def check_if_next_to(self):
        pos = self.battle_object[self.current_id].get_coordinates()
        dirs = [
            [pos[0] - 1, pos[1]],
            [pos[0] + 1, pos[1]],
            [pos[0], pos[1] - 1],
            [pos[0], pos[1] + 1],
        ]
        for dir in dirs:
            for char in self.map.mobile_collision_grid.values():
                if char[0] == dir[0] and char[1] == dir[1]:
                    return True
        return False

    def end_turn(self):
        print('end turn')
        self.load_grid_data()
        self.battle_object[self.current_id].reset_battle_stats()
        for i, x in enumerate(self.turn_order):
            if x == self.current_id:
                if i == len(self.turn_order) - 1:
                    self.current_id = self.turn_order[0]
                else:
                    self.current_id = self.turn_order[i + 1]
                break
        self.get_ui()

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        if self.ui.end_turn_button_rect.collidepoint(pos):
            self.end_turn()
        elif self.action_wheel_target:
            action_obj = self.action_wheel.handle_click(pos)
            if action_obj['val']:
                self.handle_action_wheel(action_obj)
            else:
                self.action_wheel_target = None
        else:
            # if self.player.rect.collidepoint(pos):
            #     self.action_wheel.change_target(self.player)
            #     self.action_wheel_target = self.player.id
            # else:
            for key, val in self.battle_object.items():
                if val.rect.collidepoint(pos) and key != self.current_id:
                    self.action_wheel.change_target(val)
                    self.action_wheel_target = key

    def blitme(self, screen):
        c = self.battle_object[self.current_id]
        self.map.blit_all_tiles(screen)
        for key, val in self.battle_object.items():
            val.blitme(screen)
        if c.is_party_member:
            self.map.blit_spacing_grid(screen)
        self.ui.blitme(screen)
        if c.is_party_member and c.steps_amount > 0:
            circle_radius = c.steps_amount * self.settings.tile_size + c.rect.width // 2
            pygame.draw.circle(screen, (0,0,255), c.rect.center, circle_radius, width=2)
        if self.action_wheel_target:
            self.action_wheel.blitme(screen)