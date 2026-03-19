import pygame

from character import Character

class Ally(Character):
    def __init__(self, id, pos):
        super().__init__(pos, 'human')
        self.id = id
        self.rect.x = self.size * pos[0]
        self.rect.y = self.size * pos[1]
        self.is_party_member = True
        self.speed = 4

    def handle_movement(self, key, is_down):
        if key == pygame.K_DOWN:
            self.moving_down = is_down
            self.dir = 'down' if is_down else self.dir
        if key == pygame.K_UP:
            self.moving_up = is_down
            self.dir = 'up' if is_down else self.dir
        if key == pygame.K_RIGHT:
            self.moving_right = is_down
            self.dir = 'right' if is_down else self.dir
        if key == pygame.K_LEFT:
            self.moving_left = is_down
            self.dir = 'left' if is_down else self.dir
