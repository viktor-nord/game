import pygame
from pygame.sprite import Sprite
from enum import Enum

class AnimationIndex(Enum):
    header = 'assets/ui_sprites/Sprites/Content Appear Animation/1 Headers/3'

class Animation(Sprite):
    def __init__(self, game, path, pos):
        super().__init__()
        self.path = path
        self.test = pygame.image.load('assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Folding & Cutout/2 Headers/2.png').convert_alpha()
        self.arr = self.get_img_arr(path)
        self.rect = self.arr[0].get_rect()
        self.lenght = len(self.arr)
        self.rect.x = pos[0] if pos[0] != None else self.arr[0].get_rect(center = game.screen.get_rect().center).x
        self.rect.y = pos[1] if pos[1] != None else self.arr[0].get_rect(center = game.screen.get_rect().center).y
        self.counter = 0
        self.animation_is_done = False

    def update(self):
        if self.counter < (self.lenght - 1) * 2:
            self.counter += 1
        else:
            self.animation_is_done = True


    def get_img_arr(self, path):
        index = 1
        arr = []
        while True:
            try:
                img = pygame.image.load(f'{path}/{index}.png')
            except FileNotFoundError:
                break
            else:
                arr.append(img)
                index += 1
        arr.reverse()
        arr.append(self.test)
        return arr

    def blitme(self, screen):
        screen.blit(self.arr[self.counter // 2], self.arr[self.counter // 2].get_rect(center = self.rect.center))
        # screen.blit(self.arr[self.counter // 2], self.rect)
