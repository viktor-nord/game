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
from d20 import D20

class Battle():
    def __init__(self, game):
        self.game = game
        self.name = 'battle'
        self.game_pause = False
        self.walking_animation = False
        self.allow_events = True
        self.turn_order = []
        self.id = 'player'
        self.settings = Settings()
        self.map = BattleMap()
        self.player = Player([5, 10])
        self.obj = {
            f"{self.player.id}": self.player, 
            "buddy": Ally(id='buddy', pos=(6, 11)),
            "jon": Npc('jon', (6, 3)), 
            "bob": Npc('bob', (24, 3), type='skeleton'), 
            "mike": Npc('mike', (5, 11)), 
        }
        self.dead_list = []
        self.ui = BattleUI(self, self.obj)
        self.map.load_grid_data(self.obj, self.id)
        self.action_wheel_target = None
        self.action_wheel = ActionWheel()
        self.init_battle() # call from parent instead
        self.dialog = None
        self.info = MiraclesInfoDisplay(self.player.data.miracles)
        self.set_circle(self.obj[self.id].steps_amount, self.obj[self.id].rect)
        self.d20 = D20(20)

    def init_battle(self):
        self.roll_inisiative()
        self.get_ui()
        self.map.load_grid_data(self.obj, self.id)

    def update(self):
        if self.info.active:
            self.info.update()
        else:
            if self.d20.active and self.d20.animation_active == False and not self.dialog:
                self.dialog = Dialog([f"{self.id} is attacking {self.action_wheel.current_id}"])
            if self.walking_animation:
                self.check_walking_animation()
            else:
                self.handle_turn()
            for char in self.obj.values():
                char.update()
            # self.obj[self.id].update()
            if self.action_wheel_target:
                self.action_wheel.update()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
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
        for id in self.obj.keys():
            self.turn_order.append(id)
        # dic = {}
        # for id in self.obj.keys():
        #     dic[id] = randrange(1,21)
        # self.turn_order = [k for k, v in sorted(dic.items(), key=lambda item: item[1])]
        self.id = self.turn_order[0]

    def get_ui(self):
        dic = {}
        for id in self.turn_order:
            dic[f"{id}"] = self.obj[f"{id}"]
        self.ui.__init__(self, dic, self.id)
        # self.ui = BattleUI(self, dic, self.id)

    def handle_turn(self):
        c = self.obj[self.id]
        if c.is_party_member:
            self.allow_events = True
        else:
            if c.steps_amount < 1:
                self.end_turn()
            else:
                self.obj[self.id].battle_ai()
                self.walking_animation = True

    def check_walking_animation(self):
        c = self.obj[self.id]
        x = c.rect.x / self.settings.tile_size == float(c.moving_to[0])
        y = c.rect.y / self.settings.tile_size == float(c.moving_to[1])
        if x and y:
            self.obj[self.id].reset_movement()
            self.obj[self.id].steps_amount -= 1
            self.set_circle(c.steps_amount, c.rect)
            self.get_ui()
            self.walking_animation = False
            self.map.load_grid_data(self.obj, self.id)

    def handle_click(self):
        if self.d20.active and self.d20.animation_active == False:
            self.melee_attack(self.action_wheel.current_id)
            self.d20.reset()
        pos = pygame.mouse.get_pos()
        self.ui.handle_click(pos)
        if self.dialog:
            self.dialog.next()
            if self.dialog.done:
                self.dialog = None
            return
            # self.end_turn()
        elif self.info.active:
            self.info.check_click()
            if self.info.selected_miracle:
                print(self.info.selected_miracle)
                self.info.selected_miracle = ''
        elif self.action_wheel_target:
            action_obj = self.action_wheel.handle_click(pos)
            if action_obj['val']:
                self.handle_action_wheel(action_obj)
            self.action_wheel_target = None
        else:
            for key, val in self.obj.items():
                if val.rect.collidepoint(pos) and key != self.id:
                    self.action_wheel.change_target(val)
                    self.action_wheel_target = key

    def handle_movement(self, key, is_down):
        if self.d20.active and self.d20.animation_active == False:
            self.melee_attack(self.action_wheel.current_id)
            self.d20.reset()
        c = self.obj[self.id]
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
            self.obj[self.id].moving_to = target_pos
            self.obj[self.id].handle_movement(key, True)

    def start_roll(self):
        self.d20.roll()

    def melee_attack(self, id):
        dice = self.d20.roll(show_animation=False)
        if True:
        # if dice >= self.obj[id].ac or dice == 20:
            if dice == 20:
                self.dialog = Dialog(["Criticla hit!"])
            else:
                self.dialog = Dialog([f"{self.id} is attacking {id}"])
            weapon = self.obj[self.id].primary_weapon
            damage = 20
            # damage = self.d20.roll(dice=weapon['dice'])
            self.obj[self.id].change_action('attack')
            status = self.obj[id].take_damage(damage, weapon['damage_type'], 18)
            if status == 'death':
                self.dead_list.append(self.obj[id])
                i = self.turn_order.index(id)
                del self.turn_order[i]
                del self.obj[id]
            self.action_wheel_target = None
        else:
            if dice == 0:
                self.dialog = Dialog(['Critical missed'])
            else:
                self.dialog = Dialog(['Attack missed'])

    def handle_action_wheel(self, action_obj):
        if action_obj['val'] == 'primary':
            if self.obj[self.id].actions_amount < 1:
                self.dialog = Dialog(['You have already used your action'])
                return
            target = self.get_adjesent_target(action_obj['id'])
            if target == action_obj['id']:
                self.start_roll()
                # self.melee_attack(action_obj['id'])
                self.obj[self.id].actions_amount -= 1
                self.get_ui()
            else:
                self.dialog = Dialog(['You are to far away'])
        elif action_obj['val'] == 'spell':
            self.info.active = True


    def get_adjesent_target(self, target_id):
        pos = self.obj[self.id].get_coordinates()
        for dir in get_adjasent_cord(pos).values():
            id = self.map.get_tile_collision(dir)
            if id == target_id:
                return id
        return False

    def end_turn(self):
        print(f"{self.id} ending turn")
        self.obj[self.id].reset_battle_stats()
        index = self.turn_order.index(self.id)
        self.id = self.turn_order[0 if index == len(self.turn_order) - 1 else index + 1]
        self.map.load_grid_data(self.obj, self.id)
        self.get_ui()
        self.set_circle(self.obj[self.id].steps_amount, self.obj[self.id].rect)
    
    def set_circle(self, steps, rect):
        radius = steps * self.settings.tile_size + rect.width // 2
        self.step_range_circle = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA).convert_alpha()
        pygame.draw.circle(self.step_range_circle, (0,0,255), rect.center, radius, width=2)
        self.step_range_circle.set_alpha(60)

    def blitme(self, screen):
        c = self.obj[self.id]
        self.map.blit_all_tiles(screen)
        for dead_char in self.dead_list:
            dead_char.blitme(screen)
        for char in self.obj.values():
            char.blitme(screen)
        if c.is_party_member:
            self.map.blit_spacing_grid(screen)
        self.ui.blitme(screen)
        if c.is_party_member and c.steps_amount > 0:
            screen.blit(self.step_range_circle, (0,0))
        if self.action_wheel_target:
            self.action_wheel.blitme(screen)
        self.info.blitme(screen)
        self.d20.blitme(screen)
        if self.dialog:
            self.dialog.blitme(screen)
        