import pygame
from d20 import D20

class MeleeAttack:
    def __init__(self, battle):
        self.battle = battle
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
    def __init__(self, battle):
        self.battle = battle