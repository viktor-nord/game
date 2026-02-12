import sys
import pygame

from player import Player
from settings import Settings
from start_screen import StartScreen
from character_creation import CharacterCreation
from map import Map
from npc import Npc

class Main():
    def __init__(self):
        pygame.init()
        self.running = True
        self.game_pause = True
        self.character_creation_active = False
        self.settings = Settings()
        sw, sh = self.settings.screen_width, self.settings.screen_height
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((sw, sh))
        # screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.SCALED)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Akavir: God of none')
        self.animations = pygame.sprite.Group()
        self.map = Map()
        self.player = Player(self)
        self.npc_1 = Npc(self, self.map, (1, 13), movement_pattern='random')
        self.npc_2 = Npc(self, self.map, (11, 11), movement_pattern=['right', 'down', 'up', 'left'])
        self.npc_3 = Npc(self, self.map, (11, 8))
        self.npc_group = [self.npc_1, self.npc_2, self.npc_3]
        self.start_screen = StartScreen(self)
        self.character_creation = CharacterCreation(self)

    def run(self):
        while self.running:
            self.check_event()
            if self.game_pause:
                self.update_pause_menu()
            else:
                self.update_world()
            self.animations.update()
            self.update_screen()
            self.clock.tick(60)

    def update_pause_menu(self):
        if self.character_creation_active:
            self.character_creation.update()
        else:
            self.start_screen.update()

    def update_world(self):

        self.player.update()
        # player_pos = self.player.get_coordinates()
        # self.map.mobile_collision_grid.append(player_pos)
        self.map.mobile_collision_grid = []
        for npc in self.npc_group:
            npc.check_movement()
            npc.update()
            pos = npc.get_coordinates()
            self.map.mobile_collision_grid.append(pos)

    def update_screen(self):
        self.screen.fill((100,100,100))
        if self.game_pause:
            self.blit_pause_menu()
        else:
            self.blit_world()
        pygame.display.flip()

    def blit_pause_menu(self):
        if self.character_creation_active:
            self.character_creation.blitme(self.screen)
        else:
            self.start_screen.blitme(self.screen)

    def blit_world(self):
        self.map.blit_all_tiles(self.screen)
        for npc in self.npc_group:
            self.screen.blit(npc.image, npc.rect)
        self.screen.blit(self.player.image, self.player.rect)
        self.map.blit_overlay(self.player.rect, self.screen)

    def check_event(self):
        pygame.event.set_blocked(pygame.MOUSEWHEEL)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEWHEEL:
                pass
                # scroll_down = True if event.y < 0 else False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click()
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event.key, True)
            elif event.type == pygame.KEYUP:
                self.handle_key(event.key, False)


    def handle_key(self, key, is_down):
        if self.character_creation.general_page.name_input.is_active or self.character_creation.general_page.age_input.is_active:
            if is_down:
                self.character_creation.handle_key(key)
        elif key == pygame.K_SPACE:
            if is_down:
                self.handle_action()
        elif key == pygame.K_p:
            self.game_pause = True
        elif key == pygame.K_q:
            sys.exit()
        else:
            self.handle_player_movement(key, is_down)

    def handle_player_movement(self, key, is_down):
        not_colliding = self.map.check_collision(self.player.rect)
        if not_colliding:
            self.player.handle_movement(key, is_down)

    def handle_action(self):
        gg=0
        # self.map.change_state((self.player.rect.x, self.player.rect.y))

    def handle_click(self):
        if self.game_pause == False:
            return 
        if self.character_creation_active:
            self.character_creation.handle_click()
        else:
            self.start_screen.handle_click()

if __name__ == '__main__':
    game = Main()
    game.run()
    pygame.quit()
    quit()
