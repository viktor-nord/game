import pygame

from button import Button
from animation import Animation, AnimationIndex
from font import Title

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.image = pygame.image.load('assets/ui_sprites/Sprites/Book Desk/3.png')
        self.rect = self.image.get_rect(center = game.screen_rect.center)
        self.buttons = self.generate_buttons()
        self.animation = Animation(
            game, AnimationIndex.header.value, (None, 50)
        )
        self.title = Title(
            'Akavir: God of None', 
            self.animation.rect,
            size=32,
            has_underline=True
        )
        self.fade = pygame.Surface(
            (game.screen_rect.width, game.screen_rect.height)
        )
        self.fade.fill((0, 0, 0))
        self.fade.set_alpha(160)
        self.animations = pygame.sprite.Group()
        self.animations.add(self.animation)

    def generate_buttons(self):
        texts = ['New Game', 'Load Game', 'Options']
        buttons = []
        dummy = Button(self.game, 1337, "dummy", pygame.Rect(10,10,10,10), 0)
        box = dummy.image.get_rect(center = self.game.screen_rect.center)
        box.y -= 70
        for i, button in enumerate(texts):
            buttons.append(Button(self.game, i + 1, button, box, i + 1, f"{button}-{i}"))
            box.y += 70
        return buttons

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click()

    def update(self):
        for btn in self.buttons:
            btn.update()
        self.animations.update()
    
    def handle_click(self):
        for btn in self.buttons:
            val = btn.check_click()
            if val == 1:
                self.game.character_creation_active = True
            elif val == 2:
                self.game.game_pause = False

    def blitme(self, screen):
        screen.blit(self.fade, (0, 0))
        screen.blit(self.image, self.rect)
        self.animation.blitme(screen)
        if self.animation.animation_is_done:
            self.title.blitme(screen)
        # self.game.buttons.draw(screen)
        for btn in self.buttons:
            btn.blitme(screen)
        for btn in self.buttons:
            if btn.has_tool_tip:
                btn.blit_tool_tip(screen)
