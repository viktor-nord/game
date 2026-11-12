import pygame

from character import Character

class Ally(Character):
    def __init__(self, id, pos):
        super().__init__(pos, 'human')
        self.id = id
        self.name = id
        self.rect.x = self.size * pos[0]
        self.rect.y = self.size * pos[1]
        self.is_party_member = True
        self.speed = 4
        self.data = Data()

    def handle_movement(self, key, is_down):
        if key == pygame.K_DOWN:
            self.moving_down = is_down
            self.dir = 'down' if is_down else self.dir
        if key == pygame.K_UP:
            self.moving_up = is_down
            self.dir = 'up' if is_down else self.dir
        if key == pygame.K_RIGHT:
            self.moving_right = is_down
            self.dir = 'right' if is_down else self.dir
        if key == pygame.K_LEFT:
            self.moving_left = is_down
            self.dir = 'left' if is_down else self.dir

class Data:
    def __init__(self):
        self.name = ''
        self.age = 0
        self.gender = None
        self.race = ''
        self.size = 'medium'
        self.speed = 10
        self.traits = []
        self.level = 1
        self.practice = ''
        self.faith = ''
        self.hit_die = 10
        self.proficiencies = []
        self.miracles = []
        self.stats = None
        self.max_hp = 1
        self.load()

    def load(self):
        self.name = 'buddy'
        self.race = 'human'
        self.speed = 4
        self.level = 2
        self.practice = 'monk'
        self.faith = 'luko'
        self.hit_die = 10
        self.miracles = {"save_dc": 0, "spell_modifier": 0, "cantrips": [
                0, 2, 8, 9
            ],
            "lv0": [0, 2, 8, 9],
            "lv1": [0]
        }
        self.stats = Stats()
        con_mod = 0
        self.max_hp = self.hit_die // 2 + 1 + con_mod

class Stats:
    def __init__(self):
        self.str = 10
        self.wis = 10
        self.con = 10
        self.dex = 10
        self.int = 10
        self.cha = 10
