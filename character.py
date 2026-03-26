import pygame
from settings import Settings
from font import PlainText
from character_sprite import CharacterSprite

weapons = {
    'dagger': {
        'dice': 4,
        'dice_amount': 1,
        'attack_type': 'melee',
        'damage_type': 'piercing'
    },
    'sword': {
        'dice': 6,
        'dice_amount': 1,
        'attack_type': 'melee',
        'damage_type': 'slashing'
    },
    'greatsword': {
        'dice': 6,
        'dice_amount': 2,
        'attack_type': 'melee',
        'damage_type': 'slashing'
    },
    'shortbow': {
        'dice': 6,
        'dice_amount': 1,
        'attack_type': 'range',
        'damage_type': 'piercing'
    },
}

class Character():
    def __init__(self, pos=(0,0), type="human"):
        self.type = type
        self.settings = Settings()
        self.size = self.settings.tile_size
        self.character_sprite = CharacterSprite(pos, type)
        self.is_party_member = False
        self.is_player = False
        self.rect = pygame.Rect((pos[0], pos[1]), (self.size, self.size))
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_to = None
        self.ac = 10
        self.max_hp = 10
        self.hp = 10
        self.dir = ''
        self.speed = 2
        self.max_actions_amount = 1
        self.max_bonus_action_amount = 0
        self.max_steps_amount = 30 // 10
        self.actions_amount = 1
        self.bonus_action_amount = 0
        self.steps_amount = 30 // 10 # change 30 to monster speed
        self.inventory = []
        self.collision = True
        self.coordinates = self.get_coordinates()
        self.movement = {
            'right': [1, 0],
            'down': [0, 1],
            'left': [-1, 0],
            'up': [0, -1],
        }
        self.primary_weapon = weapons['sword']

    def reset_battle_stats(self):
        self.actions_amount = self.max_actions_amount
        self.bonus_action_amount = self.max_bonus_action_amount
        self.steps_amount = self.max_steps_amount
        self.reset_movement()
        self.moving_to = None
        self.dir = ''

    def get_coordinates(self):
        x = int((self.rect.x + (self.size / 2)) / self.size)
        y = int((self.rect.y + (self.size / 2)) / self.size)
        return [x, y]

    def take_damage(self, damage, type='bludgeoning', delay=0):
        self.hp -= damage
        self.character_sprite.queue.append(delay)
        self.character_sprite.queue.append('hurt')
        if self.hp <= 0:
            self.hp = 0
            self.character_sprite.queue.append('death')
            return 'death'
        return None

    def reset_movement(self):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def change_action(self, action):
        if self.character_sprite.action != action:
            self.character_sprite.counter = 0
            self.character_sprite.frame = 0
            self.character_sprite.action = action

    def get_hitbox(self, padding=8):
        r = pygame.Rect(
            (self.rect.x + padding // 2, self.rect.y + padding // 2),
            (self.rect.width - padding, self.rect.height - padding)
        )
        return r

    # def update(self, posible_moves={'right': True, 'left': True, 'down': True, 'up': True}):
    all_moves = {'right': True, 'left': True, 'down': True, 'up': True}
    def update(self, posible_moves=all_moves):
        if self.moving_right and posible_moves['right']:
            self.rect.x += self.speed
            self.character_sprite.is_flipped = False
        if self.moving_left and posible_moves['left']:
            self.rect.x -= self.speed
            self.character_sprite.is_flipped = True
        if self.moving_down and posible_moves['down']:
            self.rect.y += self.speed
        if self.moving_up and posible_moves['up']:
            self.rect.y -= self.speed
        if self.moving_right or self.moving_left or self.moving_up or self.moving_down:
            self.change_action('walk')
        else:
            if self.character_sprite.action == 'walk':
                self.change_action('idle')
        self.coordinates = self.get_coordinates()

    def blitme(self, screen):
        self.character_sprite.blitme(screen, self.rect)
