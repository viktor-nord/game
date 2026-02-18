import pygame

from character import Character

class Player(Character):
    def __init__(self, game):
        super().__init__(game)
        # img = pygame.image.load('assets/New Piskel-1.bmp')
        # self.image = pygame.transform.scale(img, (self.size, self.size))
        self.rect.x = self.size * 8
        self.rect.y = self.size * 8
        self.speed = 4
        self.id = 'player'

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
