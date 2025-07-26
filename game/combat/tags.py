from enum import Enum


class CombatTag(Enum):
    MELEE = 'melee'
    RANGED = 'ranged'
    MAGIC = 'magic'
    SUMMON = 'summon'
    TRAP = 'trap'
    AOE = 'aoe'
    MULTISTRIKE = 'multistrike'
