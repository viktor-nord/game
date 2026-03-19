import pygame
from settings import Settings

class CharacterSprite:
    def __init__(self, pos, type):
        self.type = type
        self.settings = Settings()
        self.size = self.settings.tile_size
        self.image = pygame.Surface((160, 96), pygame.SRCALPHA).convert_alpha()
        self.frames = self.get_frames(type)
        self.counter = 0
        self.frame = 0
        self.rect = pygame.Rect((pos[0], pos[1]), (self.size, self.size))
        self.action = 'idle'
        self.is_flipped = False

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
                    img = pygame.image.load(t).convert_alpha()
                    img_scaled = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                    s.blit(img_scaled, (x, y))
                frames[key].append(s)
        return frames

    def handle_animation_counter(self):
        delay = 3
        self.frame = self.counter // delay
        if (self.counter + 1) // delay > len(self.frames[self.action]) - 1:
            self.counter = 0
            self.frame = 0
            if self.action == 'attack':
                self.action = 'idle'
        else:
            self.counter += 1

    def blitme(self, screen, rect):
        offset = rect.move(-64, -32)
        self.handle_animation_counter()
        img = pygame.transform.flip(self.frames[self.action][self.frame], self.is_flipped, False)
        screen.blit(img, offset)
