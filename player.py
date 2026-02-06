import pygame

from character import Character

class Player(Character):
    def __init__(self, game):
        super().__init__(game)
        img = pygame.image.load('assets/New Piskel-1.bmp')
        self.image = pygame.transform.scale(img, (self.size, self.size))
        self.rect.x = self.size * 10
        self.rect.y = self.size * 10
        self.speed = 4

    def handle_movement(self, key, is_down):
        if key == pygame.K_DOWN:
            self.moving_down = is_down
        if key == pygame.K_UP:
            self.moving_up = is_down
        if key == pygame.K_RIGHT:
            self.moving_right = is_down
        if key == pygame.K_LEFT:
            self.moving_left = is_down
