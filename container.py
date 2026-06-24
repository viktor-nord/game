import pygame

class Container:
    def __init__(self, content, alignment, pos=None, is_vertical=True):
        self.content = content
        self.alignment = alignment
        self.is_vertical = is_vertical
        self.pos = pos if pos else (0,0)
        if self.is_vertical:
            self.height = sum([c[1].height for c in content])
            self.width = max([c[1].width for c in content])
        self.surf = pygame.Surface((
            max([c[1].width for c in content]),
            max([c[1].height for c in content])
        ), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surf.get_rect()
        self.blit_content()

    def blit_content(self):
        if self.alignment == 'center':
            for c in self.content:
                self.surf.blit(c, c.get_rect(center = self.rect))