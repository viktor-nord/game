import pygame

from button import Button
from animation import Animation, AnimationIndex
from font import Title

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.buttons = pygame.sprite.Group()
        self.image = pygame.image.load('assets/ui_sprites/Sprites/Book Desk/3.png')
        self.rect = self.image.get_rect(center = game.screen_rect.center)
        self.generate_buttons()
        self.animation = Animation(
            game, AnimationIndex.header.value, (None, 50)
        )
        self.title = Title(
            'Akavir: God of None', 
            self.animation.rect.center, 
            has_underline=True
        )
        self.fade = pygame.Surface(
            (game.screen_rect.width, game.screen_rect.height)
        )
        self.fade.fill((0, 0, 0))
        self.fade.set_alpha(160)
        self.game.animations.add(self.animation)

    def generate_buttons(self):
        buttons = ['New Game', 'Load Game', 'Options']
        dummy = Button(self.game, 1337, "dummy", pygame.Rect(10,10,10,10))
        box = dummy.image.get_rect(center = self.game.screen_rect.center)
        box.y -= 70
        for i, button in enumerate(buttons):
            self.buttons.add(Button(self.game, i + 1, button, box))
            box.y += 70

    def update(self):
        self.buttons.update()
    
    def handle_click(self):
        for btn in self.buttons:
            id = btn.check_click()
            if id == 1:
                self.game.character_creation_active = True
            elif id == 2:
                self.game.game_pause = False


    def blitme(self):
        self.screen.blit(self.fade, (0, 0))
        self.screen.blit(self.image, self.rect)
        self.animation.blitme(self.game.screen)
        if self.animation.animation_is_done:
            self.title.blitme(self.screen)
        # self.game.buttons.draw(self.screen)
        for btn in self.buttons:
            btn.blitme()