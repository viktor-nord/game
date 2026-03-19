import math

def get_modifier(stat):
    return math.floor((stat - 10) / 2 )

class Cultist:
    def __init__(self):
        self.ac = 12
        self.max_hp = 9
        self.HP = self.max_hp
        self.speed = 60
        self.str = 11
        self.dex = 12
        self.con = 10
        self.int = 10
        self.wis = 11
        self.cha = 10
        self.proficiencies = {
            'deception': 2,
            'religion': 2
        }
        self.passive_perception = 10
        self.senses = {}
        self.damage_vulnerabilities = []
        self.damage_immunities = []
        self.condition_immunities = []
        self.challenge = 0,125
        self.exp = 25
        self.skills = [
            {
                'name': 'dark devotion',
                'desc': 'The cultist has advantage on saving throws against being charmed or frightened.'
            }
        ]
        self.actions =  {
            'scimitar': {
                'type': 'melee',
                'ac_bonus': 3,
                'range': 10,
                'target': '1',
                'damage': {
                    'dice': 6,
                    'amount': 1,
                    'bonus': 1,
                    'type': 'slashing'
                }
            }
        }

class Commoner:
    def __init__(self):
        self.ac = 10
        self.max_hp = 4
        self.HP = self.max_hp
        self.speed = 60
        self.str = 10
        self.dex = 12
        self.con = 10
        self.int = 10
        self.wis = 11
        self.cha = 10
        self.proficiencies = {
            'deception': 2,
            'religion': 2
        }
        self.passive_perception = 10
        self.senses = {}
        self.damage_vulnerabilities = []
        self.damage_immunities = []
        self.condition_immunities = []
        self.challenge = 0
        self.exp = 10
        self.skills = []
        self.actions =  {
            'improvised weapon': {
                'type': 'melee',
                'ac_bonus': 2,
                'range': 10,
                'target': '1',
                'damage': {
                    'dice': 4,
                    'amount': 1,
                    'bonus': 0,
                    'type': 'bludgeoning'
                }
            }
        }

class Goblin:
    def __init__(self):
        self.ac = 15
        self.max_hp = 7
        self.HP = self.max_hp
        self.speed = 60
        self.str = 8
        self.dex = 14
        self.con = 10
        self.int = 10
        self.wis = 8
        self.cha = 8
        self.proficiencies = {
            'stealth': 6,
        }
        self.passive_perception = 9
        self.senses = {
            'darkvision': 120
        }
        self.damage_vulnerabilities = []
        self.damage_immunities = []
        self.condition_immunities = []
        self.challenge = 0.25
        self.exp = 50
        self.skills = [
            {
                'name': 'nimble escape', 
                'desc': 'The goblin can take the Disengage or Hide action as a bonus action on each of its turns.'
            }
        ]
        self.actions =  {
            'scimitar': {
                'type': 'melee',
                'ac_bonus': 4,
                'range': 10,
                'target': '1',
                'damage': {
                    'dice': 6,
                    'amount': 1,
                    'bonus': 1,
                    'type': 'slashing'
                }
            },
            'shortbow': {
                'type': 'range',
                'ac_bonus': 4,
                'range': 160,
                'target': '1',
                'damage': {
                    'dice': 6,
                    'amount': 1,
                    'bonus': 2,
                    'type': 'piercing'
                }
            }
        }

class Skeleton:
    def __init__(self):
        self.ac = 13
        self.max_hp = 13
        self.HP = self.max_hp
        self.speed = 60
        self.str = 10
        self.dex = 14
        self.con = 15
        self.int = 6
        self.wis = 8
        self.cha = 5
        self.proficiencies = {}
        self.passive_perception = 9
        self.senses = {
            'darkvision': 120
        }
        self.damage_vulnerabilities = ['bludgeoning']
        self.damage_immunities = ['poison']
        self.condition_immunities = ['exhaustion', 'poisoned']
        self.challenge = 0.25
        self.exp = 50
        self.skills = []
        self.actions =  {
            'shortsword': {
                'type': 'melee',
                'ac_bonus': 4,
                'range': 10,
                'target': '1',
                'damage': {
                    'dice': 6,
                    'amount': 1,
                    'bonus': 2,
                    'type': 'piercing'
                }
            },
            'shortbow': {
                'type': 'range',
                'ac_bonus': 4,
                'range': 160,
                'target': '1',
                'damage': {
                    'dice': 6,
                    'amount': 1,
                    'bonus': 2,
                    'type': 'piercing'
                }
            }
        }

class Bugbear:
    def __init__(self):
        self.ac = 16
        self.max_hp = 27
        self.HP = self.max_hp
        self.speed = 60
        self.str = 15
        self.dex = 14
        self.con = 13
        self.int = 8
        self.wis = 11
        self.cha = 9
        self.proficiencies = {
            'stealth': 6,
            'survival': 2
        }
        self.passive_perception = 10
        self.senses = {
            'darkvision': 120
        }
        self.damage_vulnerabilities = []
        self.damage_immunities = []
        self.condition_immunities = []
        self.challenge = 1
        self.exp = 200
        self.skills = [
            {
                'name': 'Surprise Attack',
                'desc': 'If the bugbear surprises a creature and hits it with an attack during the first round of combat, the target takes an extra 7 (2d6) damage from the attack.'
            }
        ]
        self.actions =  {
            'morningstar': {
                'type': 'melee',
                'ac_bonus': 4,
                'range': 10,
                'target': '1',
                'damage': {
                    'dice': 8,
                    'amount': 2,
                    'bonus': 2,
                    'type': 'piercing'
                }
            },
            'javelin': {
                'type': 'melee',
                'ac_bonus': 4,
                'range': 10,
                'target': '1',
                'damage': {
                    'dice': 6,
                    'amount': 2,
                    'bonus': 2,
                    'type': 'piercing'
                }
            },
            'javelin ranged': {
                'type': 'range',
                'ac_bonus': 4,
                'range': 60,
                'target': '1',
                'damage': {
                    'dice': 6,
                    'amount': 1,
                    'bonus': 2,
                    'type': 'piercing'
                }
            }

        }
