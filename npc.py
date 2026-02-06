from character import Character
import random

class Npc(Character):
    def __init__(self, game):
        super().__init__(game)
        self.rect.x = self.size * 12
        self.rect.y = self.size * 12
        self.moving_to = None
        self.dir = 'none'

    def check_movement(self):
        if self.dir != 'none':
            return
        options = ['none', 'down', 'up', 'right', 'left']
        num = random.randrange(0, 5)
        ods_of_moving = random.randrange(0, 60)
        if ods_of_moving == 0:
            move = True
        # self.generate_dir()  
        x, y = self.get_coordinates()
        if self.dir == 'down':
            y += 1
        elif self.dir == 'up':
            y -= 1
        elif self.dir == 'right':
            x += 1
        elif self.dir == 'left':
            x -= 1
        self.moving_to = [x, y]
        
    def generate_dir(self):
        self.reset_movement()
        num = random.randrange(0, 10)
        if num == 9:
            self.moving_down = True
            self.dir = 'down'
        elif num == 8:
            self.moving_up = True
            self.dir = 'up'
        elif num == 7:
            self.moving_right = True
            self.dir = 'right'
        elif num == 6:
            self.moving_left = True
            self.dir = 'left'        
