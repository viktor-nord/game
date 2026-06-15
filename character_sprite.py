import pygame
from image import Image
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

    def get_url(self, type, hair):
        base = 'assets/tileset/Characters'
        self.mall = {
            'human': {
                'layers': ['base', hair, 'tools'],
                'actions': {'idle': 9, 'walk': 8, 'attack': 10, 'hurt': 8, 'death': 13}
            },
            'goblin': {
                'layers': ['spr'],
                'actions': {'idle': 8, 'walk': 8, 'attack': 10, 'hurt': 8, 'death': 9}
            },
            'skeleton': {
                'layers': ['skeleton'],
                'actions': {'idle': 6, 'walk': 8, 'attack': 7, 'hurt': 7, 'death': 10}
            }
        }
        return_value = {}
        for key, val in self.mall[type]['actions'].items():
            x = key.upper() if type == 'human' else 'PNG'
            return_value[key] = [f"{base}/{type.capitalize()}/{x}/{l}_{key}_strip{val}.png" for l in self.mall[type]['layers']]
        return return_value

    def get_frames(self, type):
        player_hair = 'bowlhair'
        npc_hair = 'longhair'
        new_type = 'human' if type == 'player' else type
        new_hair = player_hair if type == 'player' else npc_hair
        mall = self.get_url(new_type, new_hair)
        frames = {}
        distance_between_frames = 192
        for key, val in mall.items():
            frame_amount = self.mall[new_type]['actions'][key]
            frames[key] = []
            for i in range(frame_amount):
                s = pygame.Surface((160, 96), pygame.SRCALPHA).convert_alpha()
                x = i * distance_between_frames + 16
                for t in val:
                    s.blit(Image(t, scale=2).image, (-x, -16))
                frames[key].append(s)
        return frames

    def change_action(self, action):
        if self.action == action:
            return
        self.counter = 0
        self.frame = 0
        self.action = action

# walk - dir, infi
# idle - dir, infi
# attack - dir
# hurt - que
# death - que, speci

    def handle_animation_counter(self):
        delay = 3
        self.frame_counter = self.counter // delay
        done = (self.counter + 1) // delay == len(self.frames[self.action])
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
            img = pygame.transform.flip(
                self.frames[self.action][self.frame_counter], 
                self.is_flipped, 
                False
            )
            screen.blit(img, offset)
