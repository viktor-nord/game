import json
from random import randrange

class MeleeAttack:
    def __init__(self):
        self.message = ""
        self.attack_is_successful = False

    def reset(self):
        self.message = ""
        self.attack_is_successful = False

    def check_attack_roll(self, dice, attacker, defender, weapon):
        ac = defender.ac
        mod = self.get_mod(attacker, weapon)
        weapon_bonus = self.get_weapon_bonus(weapon)
        if dice == 20:
            self.message = "Criticla hit!"
            self.attack_is_successful = True
        elif dice == 1:
            self.message = 'Critical missed'
            self.attack_is_successful = False
        elif dice + mod + weapon_bonus >= ac:
            self.message = f"{attacker.name} is attacking {defender.name}"
            self.attack_is_successful = True
        else:
            self.message = 'Attack missed'
            self.attack_is_successful = False

    def get_mod(self, attacker, weapon):
        use_str = 'small' not in weapon['tags']
        if hasattr(attacker, "str"):
            stat = attacker.str if use_str else attacker.dex
        else:
            stat = attacker.data.stats.str if use_str else attacker.data.stats.dex
        return attacker.get_stat_mod(stat)

    def get_weapon_bonus(self, weapon):
        if hasattr(weapon, 'bonus'):
            return weapon['bonus']
        else:
            return 0

    def calc_damage(self, dice, attacker, weapon):
        mod = self.get_mod(attacker, weapon)
        bonus = self.get_weapon_bonus(weapon)
        damage = dice + mod + bonus
        return damage

class MiracleAttack:
    def __init__(self):
        self.message = ""
        self.attack_is_successful = False

    def reset(self):
        self.message = ""
        self.attack_is_successful = False

    def get_primary_skill(self, practice):
        with open("data/classes.json", "r") as db:
            data = json.load(db)
            return data[practice]['primary_skill']

    def get_miracle(self, name, level="lv0"):
        with open(f"data/miracles/{level}.json", "r") as db:
            data = json.load(db)
            val = next((x for x in data if x['name'] == name), None)
            return val

    def check_attack_roll(self, dice, attacker, defender):
        ac = defender.ac
        mod = self.get_mod(attacker)
        if dice == 20:
            self.message = "Criticla hit!"
            self.attack_is_successful = True
        elif dice == 1:
            self.message = 'Critical missed.'
            self.attack_is_successful = False
        elif dice + mod >= ac:
            self.message = f"{attacker.name} is attacking {defender.name}."
            self.attack_is_successful = True
        else:
            self.message = 'Attack missed.'
            self.attack_is_successful = False

    def get_mod(self, attacker):
        ability = self.get_primary_skill(attacker.data.practice)
        stat = attacker.data.data['stats'][ability]
        return attacker.get_stat_mod(stat)

    def calc_damage(self, attacker, miracle, miracle_level):
        mod = self.get_mod(attacker)
        spell = self.get_miracle(miracle, miracle_level)
        if spell['damage']:
            rand = randrange(1, spell['damage']['dice'] + 1) 
            dice = rand * spell['damage']['amount'] 
            return dice + mod
        else:
            return 0