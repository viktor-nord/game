import pygame

class Character():
    def __init__(self, game):
        self.game = game
        self.size = game.settings.tile_size
        self.image = pygame.Surface((160, 96), pygame.SRCALPHA).convert_alpha()
        self.frames = {}
        self.counter = 0
        self.frame = 0
        self.rect = pygame.Rect((0,0), (self.size, self.size))
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.dir = ''
        self.speed = 1
        self.inventory = []
        self.collision = True
        self.coordinates = self.get_coordinates()
        self.action = 'idle'

    def get_coordinates(self):
        x = int((self.rect.x + (self.size / 2)) / self.size)
        y = int((self.rect.y + (self.size / 2)) / self.size)
        return (x, y)

    def get_img(self, src, scale=2):
        img = pygame.image.load(src).convert_alpha()
        img_scaled = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        return img_scaled

    def reset_movement(self):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.not_colliding('right'):
            self.rect.x += self.speed
        if self.moving_left and self.not_colliding('left'):
            self.rect.x -= self.speed
        if self.moving_down and self.not_colliding('down'):
            self.rect.y += self.speed
        if self.moving_up and self.not_colliding('up'):
            self.rect.y -= self.speed
        self.coordinates = self.get_coordinates()

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
        col_1 = self.game.map.is_colliding((pos_x_1, pos_y_1), self.id)
        col_2 = self.game.map.is_colliding((pos_x_2, pos_y_2), self.id)
        if col_1 or col_2:
            not_colliding = False
        return not_colliding

    def blitme(self, screen):
        offset = self.rect.move(-64, -32)
        delay = 3
        self.frame = self.counter // delay
        if (self.counter + 1) // delay > len(self.frames[self.action]) - 1:
            self.counter = 0
            self.frame = 0
            self.action = 'idle'
        else:
            self.counter += 1

        screen.blit(self.frames[self.action][self.frame], offset)
        # pygame.draw.rect(screen, (0,0,0), self.rect)
