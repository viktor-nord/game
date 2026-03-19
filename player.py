import pygame
import json

from character import Character

class Player(Character):
    def __init__(self, pos=[13, 8]):
        super().__init__(pos, 'player')
        self.id = 'player'
        self.rect.x = self.size * pos[0]
        self.rect.y = self.size * pos[1]
        self.speed = 4
        self.moving_to = [self.rect.x, self.rect.y]
        self.data = PlayerData()
        self.max_hp = self.data.max_hp
        self.hp = self.data.max_hp
        self.steps_amount = self.data.speed // 10
        self.max_steps_amount = self.data.speed // 10
        self.is_party_member = True
        self.is_player = True

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

class PlayerData:
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
        with open("save/player.json", "r") as db:
            data = json.load(db)
        self.name = data["general"]["name"]
        self.age = data["general"]["age"]
        self.gender = data["general"]["gender"]
        self.race = data["general"]["race"]
        self.size = data["general"]["size"]
        self.speed = data["general"]["speed"]
        self.traits = data["general"]["traits"]
        self.level = data["general"]["level"]
        self.practice = data["religion"]["practice"]
        self.faith = data["religion"]["faith"]
        self.hit_die = data["religion"]["hit_die"]
        self.proficiencies = data["proficiencies"]
        self.miracles = data["miracles"]
        self.stats = PlayerStats(data["stats"])
        self.max_hp = self.hit_die // 2 + 1 + self.stats.constitution_modifier

class PlayerStats:
    def __init__(self, stats):
        self.strength = stats["strength"]
        self.wisdom = stats["wisdom"]
        self.constitution = stats["constitution"]
        self.dexterity = stats["dexterity"]
        self.intelligence = stats["intelligence"]
        self.charisma = stats["charisma"]
        self.strength_modifier = stats["strength_modifier"]
        self.wisdom_modifier = stats["wisdom_modifier"]
        self.constitution_modifier = stats["constitution_modifier"]
        self.dexterity_modifier = stats["dexterity_modifier"]
        self.intelligence_modifier = stats["intelligence_modifier"]
        self.charisma_modifier = stats["charisma_modifier"]
