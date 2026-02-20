# To Do

* change checkbox. two buttons per line

pixel perfect collision - https://www.youtube.com/watch?v=tJiKYMQJnYg

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
* bard = apostle
* druid = Guru
* rogue = virgin
* sorcerer = rabbi
* warlock = Sikh

## Spells/Miracles

### db template 
  {
    "higher_level": string,
    "index": int,
    "name": string,
    "desc": string,
    "range": string (should be int),
    "components": [string],
    "material":? string
    "ritual": bool,
    "duration": string (should be int),
    "concentration": bool,
    "casting_time": string,
    "level": int,
    "damage":? {
      "damage_type": string,
      "die": int,
      "level": {
        "1": int,
        "5": int,
        "11": int,
        "17": int
      }
    },
    "dc":? {
      "dc_type": string,
      "dc_success": string
    },
    "area_of_effect":? {
      "type": "cone",
      "size": 15
    },
    "effect":? [
      {
        "type": "disadvantage",
        "target": "target",
        "duration": "use"
      }
    ],
    "school": string,
    "classes": [string]
  }