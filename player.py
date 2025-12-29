import pygame

class Player():
    def __init__(self, game):
        self.game = game
        self.size = game.settings.tile_size
        img = pygame.image.load('assets/New Piskel-1.bmp')
        self.image = pygame.transform.scale(img, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.rect.x = self.size * 10
        self.rect.y = self.size * 10
        self.speed = 4
        self.inventory = []

    def update(self):
        if self.moving_right and self.not_colliding('right'):
            self.rect.x += self.speed
        if self.moving_left and self.not_colliding('left'):
            self.rect.x -= self.speed
        if self.moving_down and self.not_colliding('down'):
            self.rect.y += self.speed
        if self.moving_up and self.not_colliding('up'):
            self.rect.y -= self.speed

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        self.moving_down = keys[pygame.K_DOWN]
        self.moving_up = keys[pygame.K_UP]
        self.moving_right = keys[pygame.K_RIGHT]
        self.moving_left = keys[pygame.K_LEFT]

    def not_colliding(self, dir):
        size = self.size
        not_colliding = True
        x = self.rect.x + (size // 2)
        y = self.rect.y + (size // 2)
        extra = 10
        pos_x_1 = (x - extra) // size
        pos_x_2 = (x + extra) // size
        pos_y_1 = (y - extra) // size
        pos_y_2 = (y + extra) // size
        if dir == 'right':
            pos_x_1 = (x + extra + self.speed) // size
            pos_x_2 = (x + extra + self.speed) // size
        if dir == 'left':
            pos_x_1 = (x - extra - self.speed) // size
            pos_x_2 = (x - extra - self.speed) // size
        if dir == 'down':
            pos_y_1 = (y + extra + self.speed) // size
            pos_y_2 = (y + extra + self.speed) // size
        if dir == 'up':
            pos_y_1 = (y - extra - self.speed) // size
            pos_y_2 = (y - extra - self.speed) // size
        col_1 = self.game.map.is_colliding((pos_x_1, pos_y_1))
        col_2 = self.game.map.is_colliding((pos_x_2, pos_y_2))
        if col_1 or col_2:
            not_colliding = False
        return not_colliding

