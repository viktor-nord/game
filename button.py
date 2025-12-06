import pygame
from pygame.sprite import Sprite
from font import Text

class Button(Sprite):
    def __init__(self, game, id, text, pos):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.id = id
        img = pygame.image.load('assets/button.png')
        self.wh = (img.get_rect().width * 2, img.get_rect().height * 2)
        self.image = pygame.transform.scale(img, self.wh)
        self.rect = self.image.get_rect(center = pos)
        self.text = Text(text, pos)
    
    def draw_button(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text.text, self.text.rect)

    def update(self):
        pos = pygame.mouse.get_pos()
        basic = pygame.image.load('assets/button.png')
        active = pygame.image.load('assets/button_hover.png')
        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(active, self.wh)
        else:
            self.image = pygame.transform.scale(basic, self.wh)

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.game.game_pause:
            return self.id
        else:
            return False

class CheckBox(Button):
    def __init__(self, game, id, text, pos, width):
        super().__init__(game, id, text, pos)
        self.width = width
        url = "assets/ui_sprites/Sprites/Content/5 Holders/"
        self.start = pygame.image.load(url + '9.png')
        self.middle = pygame.image.load(url + '10.png')
        self.end = pygame.image.load(url + '11.png')
        self.check_box_img = pygame.image.load(url + '22.png')
        self.start_rect = self.start.get_rect()
        self.middle_rect = self.middle.get_rect()
        self.end_rect = self.end.get_rect()
        self.end_rect.right = pos[1] + width/2
        self.margin = 10
        self.image = self.render_image()
    
    def render_image(self):
        margin = 10
        surf = pygame.Surface(
            (self.width - self.check_box_img.get_width() - self.margin, self.start.get_height() )
        )
        surf_rect = surf.get_rect()
        surf.blit(self.check_box_img, (surf_rect.x, surf_rect.y))
        x = surf_rect.x + self.check_box_img.get_width() + margin
        while x < self.width:
            surf.blit(self.middle, (x, surf_rect.y))
            x += self.middle_rect.width
        surf.blit(self.end, self.end_rect)
        return surf
    
    # draw_button
    # update