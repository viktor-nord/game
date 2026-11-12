import pygame
from image import Image

class VFX(pygame.sprite.Sprite):
    def __init__(self, pos=(0,0)):
        super().__init__()
        self.counter = 0
        self.frame_counter = 0
        self.delay = 3
        self.done = False
        url = "assets/VFX/lightning_32x48.png"
        size = (32, 48)
        self.pos = pos
        self.image = Image(url).image
        self.amount_of_frames = 6
        self.frames = self.get_frames(self.image, size, self.amount_of_frames)

    def get_frames(self, img, size, amount):
        arr = []
        for x in range(amount):
            s = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
            x = x * size[0]
            s.blit(img, (-x,0))
            arr.append(s)
        return arr

    def update_frame(self):
        self.counter += 1
        self.frame_counter = self.counter // self.delay
        if self.frame_counter >= self.amount_of_frames - 1:
            self.done = True

    def blitme(self, screen):
        if self.done:
            return
        screen.blit(self.frames[self.frame_counter], self.pos)
        self.update_frame()