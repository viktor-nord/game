import pygame

from character import Character

class Player(Character):
    def __init__(self, game):
        super().__init__(game)
        self.rect.x = self.size * 8
        self.rect.y = self.size * 8
        self.speed = 4
        self.id = 'player'
        self.frames = {
            'idle': self.load_animation('idle'),
            'attack': self.load_animation('attack')
        }

    def load_animation(self, type):
        arr = []
        hair = 'bowlhair'
        url = 'assets/tileset/Characters/Human/'
        types = {
            'idle': [
                f'{url}IDLE/base_idle_strip9.png', 
                f'{url}IDLE/{hair}_idle_strip9.png',
                f'{url}IDLE/tools_idle_strip9.png',
            ],
            'attack': [
                f'{url}ATTACK/base_attack_strip10.png', 
                f'{url}ATTACK/{hair}_attack_strip10.png',
                f'{url}ATTACK/tools_attack_strip10.png',
            ]
        }
        frame_amounts = {
            'idle': 9,
            'attack': 10
        }
        distance_between_frames = 192
        for i in range(0, frame_amounts[type]):
            s = pygame.Surface((160, 96), pygame.SRCALPHA).convert_alpha()
            x = (i * distance_between_frames + 16) * -1
            y = -16
            for t in types[type]:
                img = self.get_img(t)
                s.blit(img, (x, y))
            arr.append(s)
        return arr

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
