import pygame
from character import Character
import random

class Npc(Character):
    def __init__(self, id, pos, type='goblin', movement_pattern=None):
        super().__init__()
        self.starting_position = pos
        self.prev_pos = pos
        self.rect.x = self.size * pos[0]
        self.rect.y = self.size * pos[1]
        self.type = type
        self.moving_to = None
        self.id = id
        self.dir_options = ['up', 'down', 'right', 'left']
        self.movement_pattern = movement_pattern
        self.movement_step_counter = 0
        self.frames = {
            'idle': self.load_animation('idle'),
            'attack': self.load_animation('attack')
        }

    def load_animation(self, type):
        arr = []
        if self.type == 'goblin':
            types = {
                'idle': 'assets/tileset/Characters/Goblin/PNG/spr_idle_strip9.png',
                'attack': 'assets/tileset/Characters/Goblin/PNG/spr_attack_strip10.png'
            }
        else:
            types = {
                'idle': 'assets/tileset/Characters/Skeleton/PNG/skeleton_idle_strip6.png',
                'attack': 'assets/tileset/Characters/Skeleton/PNG/skeleton_attack_strip7.png'
            }
        distance_between_frames = 192
        frame_amount = self.get_img(types[type]).get_width() / distance_between_frames
        for i in range(0, int(frame_amount)):
            s = pygame.Surface((160, 96), pygame.SRCALPHA).convert_alpha()
            x = (i * distance_between_frames + 16) * -1
            y = -16
            img = self.get_img(types[type])
            s.blit(img, (x, y))
            arr.append(s)
        return arr

    def check_movement(self, posible_moves):
        if self.movement_pattern == None:
            return
        if self.movement_pattern == 'random':
            if self.moving_to:
                self.handle_moving_to()
            else:
                self.handle_new_movement(posible_moves)
        else:
            self.handle_fixed_movement()
    
    def handle_fixed_movement(self):
        self.dir = self.movement_pattern[self.movement_step_counter]
        self.handle_dir()
        self.check_for_new_step()

    def check_for_new_step(self):
        r = self.dir == 'right' and self.rect.x > self.prev_pos[0] * self.size + self.size
        d = self.dir == 'down' and self.rect.y > self.prev_pos[1] * self.size + self.size
        l = self.dir == 'left' and self.rect.x + self.size < self.prev_pos[0] * self.size
        u = self.dir == 'up' and self.rect.y + self.size < self.prev_pos[1] * self.size
        if r or l or d or u:
            x, y = self.get_coordinates()
            self.prev_pos = [x, y]
            if self.movement_step_counter == len(self.movement_pattern) - 1:
                self.movement_step_counter = 0
            else:
                self.movement_step_counter += 1

    def handle_moving_to(self):
        if self.dir == 'down' and self.rect.y > self.moving_to[1] * self.size:
            self.rect.y = self.moving_to[1] * self.size
            self.reset_moving_to()
        elif self.dir == 'up' and self.rect.y < self.moving_to[1] * self.size:
            self.rect.y = self.moving_to[1] * self.size
            self.reset_moving_to()
        elif self.dir == 'right' and self.rect.x > self.moving_to[0] * self.size:
            self.rect.x = self.moving_to[0] * self.size
            self.reset_moving_to()
        elif self.dir == 'left' and self.rect.x < self.moving_to[0] * self.size:
            self.rect.x = self.moving_to[0] * self.size
            self.reset_moving_to()

    def reset_moving_to(self):
        self.moving_to = None
        self.reset_movement()

    def handle_dir(self):
        self.reset_movement()
        x, y = self.get_coordinates()
        if self.dir == 'down':
            self.moving_down = True
            y += 1
        elif self.dir == 'up':
            self.moving_up = True
            y -= 1
        elif self.dir == 'right':
            self.moving_right = True
            x += 1
        elif self.dir == 'left':
            self.moving_left = True
            x -= 1
        self.moving_to = [x, y]

    def handle_new_movement(self, posible_moves):
        is_moving_num = random.randrange(0, 30)
        self.dir = self.generate_dir()
        if is_moving_num > 0 or self.dir == None:
            return
        self.handle_dir()
        # r = self.rect.copy()
        # r.x += self.movement[self.dir][0] * self.speed
        # r.y = self.movement[self.dir][1] * self.speed
        if posible_moves[self.dir]:
            self.dir_options = ['up', 'down', 'right', 'left']
        else:
            self.reset_movement()
            self.dir_options.remove(self.dir)
            self.moving_to = None

    def generate_dir(self):
        if len(self.dir_options):
            return random.choice(self.dir_options)
        else:
            return None