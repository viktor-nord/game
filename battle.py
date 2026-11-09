import sys
import pygame

from player import Player
from settings import Settings
from npc import Npc
from ally import Ally
from battle_map import BattleMap
from action_wheel import ActionWheel
from battle_ui import BattleUI
from utils import get_adjasent_cord, get_key_text
from dialogs import DialogText
from miracles_info_display import MiraclesInfoDisplay
from d20 import D20
from attack_handler import MeleeAttack, MiracleAttack
from data.weapons import weapons

class Battle():
    def __init__(self, game):
        self.game = game
        self.name = 'battle'
        self.game_pause = False
        self.walking_animation = False
        self.allow_events = True
        self.turn_order = []
        self.id = 'player'
        self.action_wheel_target = None
        self.current_action = None
        self.dialog = None
        self.settings = Settings()
        self.map = BattleMap()
        self.player = Player([5, 10])
        self.obj = {
            "player": self.player, 
            "buddy": Ally(id='buddy', pos=(6, 11)),
            "jon": Npc('jon', (6, 3)), 
            "bob": Npc('bob', (24, 3), type='skeleton'), 
            "mike": Npc('mike', (5, 11)), 
        }
        self.ui = BattleUI(self, self.obj)
        self.map.load_grid_data(self.obj, self.id)
        self.action_wheel = ActionWheel()
        self.init_battle() # call from parent instead
        self.info = MiraclesInfoDisplay(self.player.data.miracles)
        self.set_circle(self.obj[self.id].steps_amount, self.obj[self.id].rect)
        self.d20 = D20(20)
        self.melee_handler = MeleeAttack(self)
        self.miracle_handler = MiracleAttack(self)

    def init_battle(self):
        self.roll_inisiative()
        self.get_ui()
        self.map.load_grid_data(self.obj, self.id)

    def update(self):
        if self.info.active:
            self.info.update()
            return
        self.update_d20_animation()
        self.update_walking_animation()
        self.update_turn()
        [char.update() for char in self.obj.values()]
        if self.action_wheel_target:
            self.action_wheel.update()

    def update_d20_animation(self):
        if self.d20.active and self.d20.animation_active == False and not self.dialog:
            self.dialog = DialogText(f"{self.id} is attacking {self.action_wheel.current_id}")

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
        if self.dialog and is_down:
            self.click_dialog()
            return
        if key == pygame.K_p and is_down:
            self.game_pause = True
        elif key == pygame.K_q and is_down:
            self.end_turn()
        elif (key == pygame.K_RIGHT or 
              key == pygame.K_LEFT or 
              key == pygame.K_UP or 
              key == pygame.K_DOWN):
            self.handle_movement(key, is_down)

    def roll_inisiative(self):
        for id in self.obj.keys():
            if id not in self.turn_order:
                self.turn_order.append(id)
        # dic = {}
        # for id in self.obj.keys():
        #     dic[id] = randrange(1,21)
        # self.turn_order = [k for k, v in sorted(dic.items(), key=lambda item: item[1])]
        self.id = self.turn_order[0]

    def get_ui(self):
        dic = {f"{id}": self.obj[f"{id}"] for id in self.turn_order}
        self.ui.__init__(self, dic, self.id)

    def update_turn(self):
        if self.walking_animation:
            return
        c = self.obj[self.id]
        if c.is_party_member:
            self.allow_events = True
        else:
            if c.steps_amount < 1 or c.is_dead:
                self.end_turn()
            else:
                self.obj[self.id].battle_ai()
                self.walking_animation = True

    def update_walking_animation(self):
        if self.walking_animation == False:
            return
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
        pos = pygame.mouse.get_pos()
        self.check_for_melee_attack()
        self.ui.handle_click(pos)
        if self.dialog:
            self.click_dialog()
        elif self.info.active:
            self.click_info(pos)
        elif self.action_wheel_target:
            self.click_action_wheel(pos)
        else:
            self.click_action_wheel_target(pos)

    def check_for_melee_attack(self):
        if self.d20.active and self.d20.animation_active == False:
            self.melee_attack(self.action_wheel.current_id)
            self.d20.reset()

    def click_dialog(self):
        if self.dialog.done:
            self.dialog = None
        else:
            self.dialog.render_all_text()

    def click_info(self, pos):
        self.info.check_click(pos)
        if self.info.selected_miracle:
            print(self.info.selected_miracle)
            self.info.selected_miracle = ''

    def click_action_wheel(self, pos):
        action_obj = self.action_wheel.handle_click(pos)
        if action_obj['val']:
            self.handle_action_wheel(action_obj)
        self.action_wheel_target = None

    def click_action_wheel_target(self,pos):
        for key, val in self.obj.items():
            if val.rect.collidepoint(pos) and key != self.id:
                self.action_wheel.change_target(val)
                self.action_wheel_target = key

    def handle_movement(self, key, is_down):
        c = self.obj[self.id]
        if self.d20.active and self.d20.animation_active == False:
            self.melee_attack(self.action_wheel.current_id)
            self.d20.reset()
        if is_down or c.steps_amount < 1:
            return
        dir = get_key_text(key)
        pos = c.get_coordinates()
        move_to = [
            pos[0] + c.movement[dir][0],
            pos[1] + c.movement[dir][1]
        ]
        if self.walking_animation == False and move_to in self.map.available_tiles:
            self.walking_animation = True
            self.obj[self.id].moving_to = move_to
            self.obj[self.id].handle_movement(key, True)

    def start_roll(self):
        self.d20.roll()

    def melee_attack(self, id):
        dice = self.d20.roll(show_animation=False)
        dice = 19
        attacker = self.obj[self.id]
        target = self.obj[self.action_wheel.current_id]
        weapon = weapons['+1 sword']
        self.melee_handler.check_attack_roll(dice, attacker, target, weapon)
        self.dialog = DialogText(self.melee_handler.message)
        if self.melee_handler.attack_is_successful:
            damage = self.melee_handler.calc_damage()
            self.obj[self.id].character_sprite.change_action('attack')
            self.obj[id].take_damage(damage, delay=18)
            self.action_wheel_target = None
        self.melee_handler.reset()

    def handle_action_wheel(self, action_obj):
        if action_obj['val'] == 'primary':
            if self.obj[self.id].actions_amount < 1:
                self.dialog = DialogText('You have already used your action')
                return
            m = self.map.mobile_collision_grid
            if m[action_obj['id']] in get_adjasent_cord(m['player']).values():
                self.start_roll()
                self.obj[self.id].actions_amount -= 1
                self.get_ui()
            else:
                self.dialog = DialogText('You are to far away')
        elif action_obj['val'] == 'spell':
            self.info.active = True

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
        wh = (self.settings.screen_width, self.settings.screen_height)
        self.step_range_circle = pygame.Surface(wh, pygame.SRCALPHA).convert_alpha()
        pygame.draw.circle(self.step_range_circle, pygame.Color(0,0,255,60), rect.center, radius, width=2)

    def blitme(self, screen):
        c = self.obj[self.id]
        self.map.blit_all_tiles(screen)
        [char.blitme(screen) for char in self.obj.values()]
        self.ui.blitme(screen)
        if c.is_party_member and c.steps_amount > 0:
            self.map.blit_spacing_grid(screen)
            screen.blit(self.step_range_circle, (0,0))
        if self.action_wheel_target:
            self.action_wheel.blitme(screen)
        self.info.blitme(screen)
        self.d20.blitme(screen)
        if self.dialog:
            self.dialog.blitme(screen)
        