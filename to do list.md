# To Do

* change checkbox. two buttons per line

pixel perfect collision - https://www.youtube.com/watch?v=tJiKYMQJnYg

# DnD rules
calc attack damage
melee = strength modifyer
range = dexterity modifyer
magic = depends

# Akavir

## changes
fighters have no fighting style. but get +1 to all weapons.
half-elf - Half-Elf Versatility ersatt med +5 speed
half-elf - abi +1 på två valfria, ersatt med +1 int

"sleight of hand" -> "finesse"
"animal handeling" -> "animals" 

## classes/Practice

monk spelslot:
0 = ki points
1 = martial arts die
2 unarmored movement

barbarian spelslot
0 = rages amount
1 = + rage damage

rogue spelslot
sneak attack 
0 = amount of d6

* cleric = cleric
* wizard = imam
* paladin = paladin
* fighter = prest
* monk = monk
* barbarian = martyr
* bard = gospel
* druid = Guru
* rogue = virgin
* sorcerer = rabbi
* warlock = Sikh

## Spells/Miracles

### db template 
  {
    "name": "",
    "desc": "",
    "range": 0,
    "material": "",
    "ritual": false,
    "duration": "",
    "concentration": false,
    "casting_time": "",
    "level": 0,
    "damage": {
      "damage_type": "",
      "dice": 0,
      "level": [1,2,3,4]
    },
    "dc": {
      "dc_type": "",
      "dc_success": {
        "damage": [0, 0],
        "effect": {
          "type": "",
          "target": "",
          "duration": ""
        }
      }
    },
    "area_of_effect": {
      "type": "",
      "size": 0
    },
    "effect": [
      {
        "type": "",
        "target": "",
        "duration": ""
      }
    ],
    "school": "",
    "classes": [""]
  },
