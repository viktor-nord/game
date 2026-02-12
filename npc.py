from tkinter import NO
from character import Character
import random

class Npc(Character):
    def __init__(self, game, map, pos, movement_pattern=None):
        super().__init__(game)
        self.starting_position = pos
        self.prev_pos = pos
        self.rect.x = self.size * pos[0]
        self.rect.y = self.size * pos[1]
        self.moving_to = None
        self.dir = ''
        self.map = map
        self.dir_options = ['up', 'down', 'right', 'left']
        self.movement_pattern = movement_pattern
        self.movement_step_counter = 0

    def check_movement(self):
        if self.movement_pattern == None:
            return
        if self.movement_pattern == 'random':
            if self.moving_to:
                self.handle_moving_to()
            else:
                self.handle_new_movement()
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

    def handle_new_movement(self):
        is_moving_num = random.randrange(0, 30)
        if is_moving_num > 0:
            return
        self.dir = self.generate_dir()
        self.handle_dir()
        if self.map.is_colliding(self.moving_to):
            self.reset_movement()
            self.dir_options.remove(self.dir)
            self.moving_to = None
        else:
            self.dir_options = ['up', 'down', 'right', 'left']
        
    def generate_dir(self):
        return random.choice(self.dir_options)
