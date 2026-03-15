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
from utils import get_adjasent_cord, get_key_text
from dialogs import Dialog
from info_display import MiraclesInfoDisplay

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
        self.map.load_grid_data(self.battle_object, self.current_id)
        self.action_wheel_target = None
        self.action_wheel = ActionWheel()
        self.init_battle() # call from parent instead
        self.dialog = None
        self.info = MiraclesInfoDisplay(self.player.data.miracles)

    def init_battle(self):
        self.roll_inisiative()
        self.get_ui()
        self.map.load_grid_data(self.battle_object, self.current_id)

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
        self.info.update()

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
        if self.dialog:
            if is_down:
                self.dialog.next()
                if self.dialog.done:
                    self.dialog = None
            return
        if key == pygame.K_p and is_down:
            self.game_pause = True
        elif key == pygame.K_q and is_down:
            self.end_turn()
        elif key == pygame.K_RIGHT or key == pygame.K_LEFT or key == pygame.K_UP or key == pygame.K_DOWN:
            self.handle_movement(key, is_down)

    def roll_inisiative(self):
        for id in self.battle_object.keys():
            self.turn_order.append(id)
        # dic = {}
        # for id in self.battle_object.keys():
        #     dic[id] = randrange(1,21)
        # self.turn_order = [k for k, v in sorted(dic.items(), key=lambda item: item[1])]
        self.current_id = self.turn_order[0]

    def get_ui(self):
        dic = {}
        for id in self.turn_order:
            dic[f"{id}"] = self.battle_object[f"{id}"]
        self.ui = BattleUI(dic, self.current_id)

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

    def check_walking_animation(self):
        c = self.battle_object[self.current_id]
        x = c.rect.x / self.settings.tile_size == float(c.moving_to[0])
        y = c.rect.y / self.settings.tile_size == float(c.moving_to[1])
        if x and y:
            self.battle_object[self.current_id].reset_movement()
            self.battle_object[self.current_id].steps_amount -= 1
            self.get_ui()
            self.walking_animation = False
            self.map.load_grid_data(self.battle_object, self.current_id)

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        if self.dialog:
            self.dialog.next()
            if self.dialog.done:
                self.dialog = None
            return
        self.info.check_click()
        if self.ui.end_turn_button_rect.collidepoint(pos):
            self.end_turn()
        elif self.action_wheel_target:
            action_obj = self.action_wheel.handle_click(pos)
            if action_obj['val']:
                self.handle_action_wheel(action_obj)
            else:
                self.action_wheel_target = None
        else:
            for key, val in self.battle_object.items():
                if val.rect.collidepoint(pos) and key != self.current_id:
                    self.action_wheel.change_target(val)
                    self.action_wheel_target = key

    def handle_movement(self, key, is_down):
        c = self.battle_object[self.current_id]
        if is_down or c.steps_amount < 1:
            return
        pos = [c.rect.x // self.settings.tile_size, c.rect.y // self.settings.tile_size]
        is_moving = False
        dir = get_key_text(key)
        target_pos = get_adjasent_cord(pos, dir)
        if target_pos in self.map.available_tiles:
            is_moving = True
        if self.walking_animation == False and is_moving:
            self.walking_animation = True
            self.battle_object[self.current_id].moving_to = target_pos
            self.battle_object[self.current_id].handle_movement(key, True)

    def melee_attack(self, id):
        self.current_id # person attacking
        if id in self.battle_object:
            self.battle_object[id].take_damage(1, 'bludgeoning')
            self.dialog = Dialog([f"{self.current_id} is attacking {id}"])
            # print(f"{self.current_id} is attacking {id}")
        else:
            print("somthing wrong in battle/melee_attack")

    def handle_action_wheel(self, action_obj):
        if action_obj['val'] == 'primary':
            if self.battle_object[self.current_id].actions_amount < 1:
                print('You have already used your action')
                return
            target = self.get_adjesent_target(action_obj['id'])
            if target == action_obj['id']:
                self.melee_attack(action_obj['id'])
                self.battle_object[self.current_id].actions_amount -= 1
                self.get_ui()
            else:
                print("you are to far away")
        elif action_obj['val'] == 'spell':
            self.info.active = True


    def get_adjesent_target(self, target_id):
        pos = self.battle_object[self.current_id].get_coordinates()
        for dir in get_adjasent_cord(pos).values():
            id = self.map.get_tile_collision(dir)
            if id == target_id:
                return id
        return False

    def end_turn(self):
        print(f"{self.current_id} ending turn")
        self.battle_object[self.current_id].reset_battle_stats()
        index = self.turn_order.index(self.current_id)
        self.current_id = self.turn_order[0 if index == len(self.turn_order) - 1 else index + 1]
        self.map.load_grid_data(self.battle_object, self.current_id)
        self.get_ui()

    def blitme(self, screen):
        c = self.battle_object[self.current_id]
        self.map.blit_all_tiles(screen)
        for char in self.battle_object.values():
            char.blitme(screen)
        if c.is_party_member:
            self.map.blit_spacing_grid(screen)
        self.ui.blitme(screen)
        if c.is_party_member and c.steps_amount > 0:
            circle_radius = c.steps_amount * self.settings.tile_size + c.rect.width // 2
            pygame.draw.circle(screen, (0,0,255), c.rect.center, circle_radius, width=2)
        if self.action_wheel_target:
            self.action_wheel.blitme(screen)
        self.info.blitme(screen)
        if self.dialog:
            self.dialog.blitme(screen)