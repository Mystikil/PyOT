from enum import IntEnum
import random


class MonsterRank(IntEnum):
    """Enumeration of dynamic monster ranks."""
    MINION = 0
    ELITE = 1
    CHAMPION = 2
    BOSS = 3
    OVERLORD = 4


RANK_CONFIG = {
    MonsterRank.MINION: {
        "name": "Minion",
        "hp": 1.0,
        "damage": 1.0,
        "speed": 1.0,
        "exp": 1.0,
    },
    MonsterRank.ELITE: {
        "name": "Elite",
        "hp": 1.5,
        "damage": 1.5,
        "speed": 1.05,
        "exp": 1.5,
    },
    MonsterRank.CHAMPION: {
        "name": "Champion",
        "hp": 2.0,
        "damage": 2.0,
        "speed": 1.1,
        "exp": 2.0,
    },
    MonsterRank.BOSS: {
        "name": "Boss",
        "hp": 3.0,
        "damage": 3.0,
        "speed": 1.15,
        "exp": 3.0,
    },
    MonsterRank.OVERLORD: {
        "name": "Overlord",
        "hp": 4.0,
        "damage": 4.0,
        "speed": 1.2,
        "exp": 5.0,
    },
}


def roll_rank(chances):
    """Return a :class:`MonsterRank` based on ``chances`` dict."""
    if not chances:
        return MonsterRank.MINION

    r = random.random()
    total = 0.0
    # iterate from highest rank to lowest
    for rank in sorted(chances.keys(), key=lambda r: r.value, reverse=True):
        total += chances[rank]
        if r < total:
            return rank
    return MonsterRank.MINION


def apply_rank(monster):
    """Apply a dynamic rank to ``monster``."""
    chances = getattr(monster.base, "rank_chances", {})
    rank = roll_rank(chances)
    monster.rank = rank
    cfg = RANK_CONFIG[rank]

    if rank != MonsterRank.MINION:
        monster.data["name"] += f" [{cfg['name']}]"

    # health & speed
    monster.data["healthmax"] = int(monster.data["healthmax"] * cfg["hp"])
    monster.data["health"] = monster.data["healthmax"]
    monster.speed = float(monster.speed * cfg["speed"])

    monster.damage_multiplier = cfg["damage"]
    monster.exp_reward = int(monster.base._experience * cfg["exp"])
    return monster
