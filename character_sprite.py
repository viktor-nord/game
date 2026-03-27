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
        self.frame_counter = 0
        self.rect = pygame.Rect((pos[0], pos[1]), (self.size, self.size))
        self.action = 'idle'
        self.queue = []
        self.single_animation = ['attack', 'hurt']
        self.is_flipped = False
        self.is_dead = False
        self.skull_image = self.frames['death'][-1]

    def get_frames(self, type):
        url = 'assets/tileset/Characters/'
        hair = 'bowlhair'
        npc_hair = 'longhair'
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
                ],
                'hurt': [
                    f'{url}Human/HURT/base_hurt_strip8.png', 
                    f'{url}Human/HURT/{hair}_hurt_strip8.png',
                    f'{url}Human/HURT/tools_hurt_strip8.png',
                ],
                'death': [
                    f'{url}Human/DEATH/base_death_strip13.png', 
                    f'{url}Human/DEATH/{hair}_death_strip13.png',
                    f'{url}Human/DEATH/tools_death_strip13.png',
                ]
            },
            'human': {
                'idle': [
                    f'{url}Human/IDLE/base_idle_strip9.png',
                    f'{url}Human/IDLE/{npc_hair}_idle_strip9.png',
                    f'{url}Human/IDLE/tools_idle_strip9.png'
                ],
                'walk': [
                    f'{url}Human/WALKING/base_walk_strip8.png', 
                    f'{url}Human/WALKING/{npc_hair}_walk_strip8.png',
                    f'{url}Human/WALKING/tools_walk_strip8.png',
                ],
                'attack': [
                    f'{url}Human/ATTACK/base_attack_strip10.png', 
                    f'{url}Human/ATTACK/{npc_hair}_attack_strip10.png',
                    f'{url}Human/ATTACK/tools_attack_strip10.png',
                ],
                'hurt': [
                    f'{url}Human/HURT/base_hurt_strip8.png', 
                    f'{url}Human/HURT/{npc_hair}_hurt_strip8.png',
                    f'{url}Human/HURT/tools_hurt_strip8.png',
                ],
                'death': [
                    f'{url}Human/DEATH/base_death_strip13.png', 
                    f'{url}Human/DEATH/{npc_hair}_death_strip13.png',
                    f'{url}Human/DEATH/tools_death_strip13.png',
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
                ],
                'hurt': [
                    f'{url}Goblin/PNG/spr_hurt_strip8.png', 
                ],
                'death': [
                    f'{url}Goblin/PNG/spr_death_strip9.png',
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
                ],
                'hurt': [
                    f'{url}Skeleton/PNG/skeleton_hurt_strip7.png', 
                ],
                'death': [
                    f'{url}Skeleton/PNG/skeleton_death_strip10.png',
                ]
            }
        }
        distance_between_frames = 192
        for key, val in mall[type].items():
            # frame_amount = int(pygame.image.load(val[0]).convert().get_width() / distance_between_frames)
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
        self.frame_counter = self.counter // delay
        done = (self.counter + 1) // delay == len(self.frames[self.action])
        # if self.is_dead:
        #     return
        if len(self.queue):
            if self.queue[0] in self.frames.keys():
                if self.action == self.queue[0]:
                    if done:
                        self.is_dead = self.action == 'death'
                        del self.queue[0]
                    else:
                        self.counter += 1
                else:
                    self.counter = 0
                    self.frame_counter = 0
                    self.action = self.queue[0]
            else:
                self.queue[0] -= 1
                if self.queue[0] == 0:
                    del self.queue[0]
        else:
            if done:
                # if self.action == 'death':
                #     self.is_dead = True
                # else:
                self.counter = 0
                self.frame_counter = 0
                if self.action in self.single_animation:
                    self.action = 'idle'
            else:
                self.counter += 1

    def blitme(self, screen, rect):
        offset = rect.move(-64, -32)
        if self.is_dead:
            screen.blit(self.skull_image, offset)
        else:
            self.handle_animation_counter()
            img = pygame.transform.flip(self.frames[self.action][self.frame_counter], self.is_flipped, False)
            screen.blit(img, offset)
