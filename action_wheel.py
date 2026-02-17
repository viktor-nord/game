import pygame

class ActionWheel:
    def __init__(self, player_rect):
        self.player_rect = player_rect
        self.options = ['melee', 'spell', 'move', 'items', 'bonus', 'dodge', 'talk', 'disengage']
        url = "assets/ui_sprites/ActionWheel/"
        curl = "assets/ui_sprites/Sprites/Content/"
        self.base_image = self.get_image(f"{url}base_action_wheel.png", True)
        self.base_top_right_image = self.get_image(f"{url}action_wheel_topright.png", True)
        self.base_top_left_image = self.get_image(f"{url}action_wheel_topleft.png", True)
        self.holder_image = self.get_image(f"{curl}5 Holders/24.png")
        self.attack_image = self.get_image(f"{curl}1 Items/1.png")
        self.move_image = self.get_image(f"{curl}1 Items/2.png")
        self.base_rect = self.base_image.get_rect()
        self.image = pygame.Surface((self.base_rect.width, self.base_rect.height), pygame.SRCALPHA).convert_alpha()
        self.image.blit(self.base_image, (0,0))
        self.rect = self.image.get_rect(center = player_rect.center)
        self.holder_top_right_rect = self.holder_image.get_rect(center = (player_rect.centerx + 18, player_rect.centery - 48))
        self.holder_top_left_rect = self.holder_image.get_rect(center = (player_rect.centerx - 20, player_rect.centery - 48))
        self.item_top_right_rect = self.attack_image.get_rect(center = self.holder_top_right_rect.center)
        self.item_top_left_rect = self.attack_image.get_rect(center = self.holder_top_left_rect.center)
        self.active_option = ''
        self.action = ''

    def get_image(self, src, big=False):
        if big:
            base = pygame.image.load(src).convert_alpha()
            return pygame.transform.scale(base, (base.get_width() * 2, base.get_height() * 2))
        else:
            return pygame.image.load(src).convert_alpha()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.active_option = self.check_collision(pos)

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        self.action = self.check_collision(pos)

    def check_collision(self, pos):
        val = ''
        if self.holder_top_right_rect.collidepoint(pos):
            val = 'melee'
        if self.holder_top_left_rect.collidepoint(pos):
            val = 'move'
        return val


    def blitme(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.holder_image, self.holder_top_right_rect)
        screen.blit(self.holder_image, self.holder_top_left_rect)
        screen.blit(self.attack_image, self.item_top_right_rect)
        screen.blit(self.move_image, self.item_top_left_rect)
        if self.active_option == 'melee':
            screen.blit(self.base_top_right_image, self.base_top_right_image.get_rect(center = self.player_rect.center))
        if self.active_option == 'move':
            screen.blit(self.base_top_left_image, self.base_top_left_image.get_rect(center = self.player_rect.center))