import pygame

from button import Button
from animation import Animation, AnimationIndex
from font import Title
from settings import Settings

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.setting = Settings()
        self.name = 'start_screen'
        self.image = pygame.image.load('assets/ui_sprites/Sprites/Book Desk/3.png')
        self.rect = self.image.get_rect(center = self.setting.center)
        self.buttons = self.generate_buttons()
        self.animation = Animation(
            AnimationIndex.header.value, pygame.Rect((self.rect.centerx, 100), (0,0))
        )
        self.title = Title(
            'Akavir: God of None', 
            self.animation.rect,
            size=32,
            has_underline=True
        )
        self.animations = pygame.sprite.Group()
        self.animations.add(self.animation)

    def generate_buttons(self):
        texts = ['New Game', 'Load Game', 'Options']
        buttons = []
        dummy = Button(1337, "dummy", pygame.Rect(10,10,10,10), 0)
        box = dummy.surf.get_rect(center = self.rect.center)
        box.y -= 70
        for i, button in enumerate(texts):
            buttons.append(Button(i + 1, button, box, i + 1, f"{button}-{i}"))
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
                self.game.mode =  'character_creation'
            elif val == 2:
                self.game.mode = 'over_world'

    def blitme(self, screen):
        screen.blit(self.image, self.rect)
        self.animation.blitme(screen)
        if self.animation.animation_is_done:
            self.title.blitme(screen)
        for btn in self.buttons:
            btn.blitme(screen)
        for btn in self.buttons:
            if btn.has_tool_tip:
                btn.tool_tip.blitme(screen)
