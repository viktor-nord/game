import pygame
from settings import Settings
from font import PlainText

class Character():
    def __init__(self, pos=(0,0), type="human"):
        self.type = type
        self.settings = Settings()
        self.size = self.settings.tile_size
        self.image = pygame.Surface((160, 96), pygame.SRCALPHA).convert_alpha()
        self.frames = self.get_frames(type)
        self.counter = 0
        self.frame = 0
        self.is_party_member = False
        self.is_player = False
        self.rect = pygame.Rect((pos[0], pos[1]), (self.size, self.size))
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_to = None
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
        self.action = 'idle'
        self.movement = {
            'right': [1, 0],
            'down': [0, 1],
            'left': [-1, 0],
            'up': [0, -1],
        }
        self.is_flipped = False
        self.animation_avtive = False

    def reset_battle_stats(self):
        self.actions_amount = self.max_actions_amount
        self.bonus_action_amount = self.max_bonus_action_amount
        self.steps_amount = self.max_steps_amount
        self.reset_movement()
        self.moving_to = None
        self.dir = ''

    def get_frames(self, type):
        url = 'assets/tileset/Characters/'
        hair = 'bowlhair'
        frames = {}
        mall = {
            'player': {
                'idle': [
                    f'{url}Human/IDLE/base_idle_strip9.png',
                    f'{url}Human/IDLE/{hair}_idle_strip9.png',
                    f'{url}Human/IDLE/tools_idle_strip9.png'
                ],
                'walk': [
                    f'{url}Human/WALKING/base_walk_strip8.png', 
                    f'{url}Human/WALKING/{hair}_walk_strip8.png',
                    f'{url}Human/WALKING/tools_walk_strip8.png',
                ],
                'attack': [
                    f'{url}Human/ATTACK/base_attack_strip10.png', 
                    f'{url}Human/ATTACK/{hair}_attack_strip10.png',
                    f'{url}Human/ATTACK/tools_attack_strip10.png',
                ]
            },
            'human': {
                'idle': [
                    f'{url}Human/IDLE/base_idle_strip9.png',
                    #f'{url}Human/IDLE/spikeyhair_idle_strip9.png',
                    f'{url}Human/IDLE/tools_idle_strip9.png'
                ],
                'walk': [
                    f'{url}Human/WALKING/base_walk_strip8.png', 
                    #f'{url}Human/WALKING/spikeyhair_walk_strip8.png',
                    f'{url}Human/WALKING/tools_walk_strip8.png',
                ],
                'attack': [
                    f'{url}Human/ATTACK/base_attack_strip10.png', 
                    #f'{url}Human/ATTACK/spikeyhair_attack_strip10.png',
                    f'{url}Human/ATTACK/tools_attack_strip10.png',
                ]
            },
            'goblin': {
                'idle': [
                    f'{url}Goblin/PNG/spr_idle_strip8.png',
                ],
                'walk': [
                    f'{url}Goblin/PNG/spr_walk_strip8.png', 
                ],
                'attack': [
                    f'{url}Goblin/PNG/spr_attack_strip10.png', 
                ]
            },
            'skeleton': {
                'idle': [
                    f'{url}Skeleton/PNG/skeleton_idle_strip6.png',
                ],
                'walk': [
                    f'{url}Skeleton/PNG/skeleton_walk_strip8.png', 
                ],
                'attack': [
                    f'{url}Skeleton/PNG/skeleton_attack_strip7.png', 
                ]
            }
        }
        distance_between_frames = 192
        for key, val in mall[type].items():
            frame_amount = int(val[0][-6:-4].replace('p',''))
            frames[key] = []
            for i in range(frame_amount):
                s = pygame.Surface((160, 96), pygame.SRCALPHA).convert_alpha()
                x = (i * distance_between_frames + 16) * -1
                y = -16
                for t in val:
                    img = self.get_img(t)
                    s.blit(img, (x, y))
                frames[key].append(s)
        return frames       

    def get_coordinates(self):
        x = int((self.rect.x + (self.size / 2)) / self.size)
        y = int((self.rect.y + (self.size / 2)) / self.size)
        return [x, y]

    def get_img(self, src, scale=2):
        img = pygame.image.load(src).convert_alpha()
        img_scaled = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        return img_scaled

    def take_damage(self, damage=1, type='bludgeoning'):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def reset_movement(self):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def change_action(self, action):
        if self.action != action:
            self.counter = 0
            self.frame = 0
            self.action = action

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
            self.is_flipped = False
        if self.moving_left and posible_moves['left']:
            self.rect.x -= self.speed
            self.is_flipped = True
        if self.moving_down and posible_moves['down']:
            self.rect.y += self.speed
        if self.moving_up and posible_moves['up']:
            self.rect.y -= self.speed
        if self.moving_right or self.moving_left or self.moving_up or self.moving_down:
            self.change_action('walk')
        else:
            if self.action == 'walk':
                self.change_action('idle')
        self.coordinates = self.get_coordinates()

    def handle_animation_counter(self):
        delay = 3
        self.frame = self.counter // delay
        if self.action == 'attack':
            print('wehe')
        if (self.counter + 1) // delay > len(self.frames[self.action]) - 1:
            self.counter = 0
            self.frame = 0
            if self.action == 'attack':
                self.action = 'idle'
        else:
            self.counter += 1

    def blitme(self, screen):
        offset = self.rect.move(-64, -32)
        self.handle_animation_counter()
        if self.is_flipped:
            img = pygame.transform.flip(self.frames[self.action][self.frame], True, False)
            screen.blit(img, offset)
        else:
            screen.blit(self.frames[self.action][self.frame], offset)

class BattleCharacter(Character):
    def __init__(self, pos, type="human"):
        super().__init__(pos, type)
        self.frames = {}
        self.counter = 0
        self.frame = 0
        self.is_party_member = False
        self.is_player = False
        self.rect = pygame.Rect((pos[0], pos[1]), (self.size, self.size))
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_to = None
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
        self.action = 'idle'
        self.movement = {
            'right': [1, 0],
            'down': [0, 1],
            'left': [-1, 0],
            'up': [0, -1],
        }
        self.is_flipped = False
        self.animation_avtive = False
        self.name_tag = PlainText(f"{self.id}")
