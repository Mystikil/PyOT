"""Utility classes and helpers for item rarity handling."""

"""Utility classes and helpers for item rarity handling."""

from enum import IntEnum
import random
import time
import os
import json
import game.const

# Load list of item ids that should not receive random rarity.
_EXCLUSION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'data', 'rarity_exclusions.json')
try:
    with open(_EXCLUSION_FILE) as f:
        EXCLUDED_ITEM_IDS = set(json.load(f))
except Exception:
    EXCLUDED_ITEM_IDS = set()


class Rarity(IntEnum):
    """Enumeration of the 17 item rarity levels."""

    JUNK = 0
    UNCOMMON = 1
    COMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
    MASTER_CRAFTED = 6
    MYTHFORGED = 7
    ECLIPSEBORN = 8
    DREADNAUGHT_RELIC = 9
    CELESTIUM_CLASS = 10
    WYRMSHADOW = 11
    OBLIVION_TOUCHED = 12
    ASHEN_KINGS_LEGACY = 13
    VEILPIERCER = 14
    PRIMORDIAL_SIGIL = 15
    GODREND = 16


# ---------------------------------------------------------------------------
# RARITY CONFIGURATION
# ---------------------------------------------------------------------------

RARITY_CONFIG = {
    Rarity.JUNK:             {"name": "Junk",              "multiplier": 1.0,  "dropChance": 0.40},
    Rarity.UNCOMMON:         {"name": "Uncommon",          "multiplier": 1.05, "dropChance": 0.25},
    Rarity.COMMON:           {"name": "Common",            "multiplier": 1.10, "dropChance": 0.15},
    Rarity.RARE:             {"name": "Rare",              "multiplier": 1.20, "dropChance": 0.08},
    Rarity.EPIC:             {"name": "Epic",              "multiplier": 1.30, "dropChance": 0.05},
    Rarity.LEGENDARY:        {"name": "Legendary",         "multiplier": 1.45, "dropChance": 0.03},
    Rarity.MASTER_CRAFTED:   {"name": "Master Crafted",    "multiplier": 1.60, "dropChance": 0.015},
    Rarity.MYTHFORGED:       {"name": "Mythforged",        "multiplier": 1.75, "dropChance": 0.010},
    Rarity.ECLIPSEBORN:      {"name": "Eclipseborn",       "multiplier": 1.90, "dropChance": 0.007},
    Rarity.DREADNAUGHT_RELIC:{"name": "Dreadnaught Relic", "multiplier": 2.05, "dropChance": 0.004},
    Rarity.CELESTIUM_CLASS:  {"name": "Celestium-Class",   "multiplier": 2.20, "dropChance": 0.003},
    Rarity.WYRMSHADOW:       {"name": "Wyrmshadow",        "multiplier": 2.40, "dropChance": 0.002},
    Rarity.OBLIVION_TOUCHED: {"name": "Oblivion-Touched",  "multiplier": 2.60, "dropChance": 0.0015},
    Rarity.ASHEN_KINGS_LEGACY:{"name": "Ashen King's Legacy","multiplier": 2.80, "dropChance": 0.0010},
    Rarity.VEILPIERCER:      {"name": "Veilpiercer",       "multiplier": 3.00, "dropChance": 0.0007},
    Rarity.PRIMORDIAL_SIGIL: {"name": "Primordial Sigil",  "multiplier": 3.50, "dropChance": 0.0004},
    Rarity.GODREND:          {"name": "Godrend",           "multiplier": 4.00, "dropChance": 0.0002},
}

# Rarities at or above this level are considered ``high`` and will
# trigger special notifications when dropped by monsters.
HIGH_RARITY_THRESHOLD = Rarity.CELESTIUM_CLASS

# Visual effect played at the drop position for high-rarity loot.
# Uses the numeric constant from :mod:`game.const`.
HIGH_RARITY_EFFECT = game.const.EFFECT_FIREWORK_BLUE

# Message template sent to the killer when a high-rarity item is looted.
HIGH_RARITY_MESSAGE = "\U0001F525 You looted a {rarity} {item}!"


def assign_rarity():
    """Return a random :class:`Rarity` based on configured drop chances."""

    rarities = list(RARITY_CONFIG.keys())
    weights = [RARITY_CONFIG[r]["dropChance"] for r in rarities]
    return random.choices(rarities, weights=weights, k=1)[0]


def apply_rarity_to_item(item):
    """Assign a rarity to ``item`` and scale its stats accordingly."""

    if item.itemId in EXCLUDED_ITEM_IDS:
        return item

    rarity = assign_rarity()
    cfg = RARITY_CONFIG[rarity]

    # tag rarity identifier
    item.rarity = rarity

    # unique serial used for descriptive purposes only
    serial = f"{int(time.time()*1000)}{random.randint(1000,9999)}"
    item.rarity_serial = serial

    # store rarity description separately so we don't override the
    # Item.description() method which many parts of the code rely on
    item.rarity_description = f"Rarity: {cfg['name']}"

    # scale primary combat stats
    mult = cfg["multiplier"]
    for attr in ("attack", "defense", "defence", "armor"):
        value = getattr(item, attr, None)
        if isinstance(value, (int, float)):
            setattr(item, attr, int(round(value * mult)))

    return item


def is_high_rarity(rarity):
    """Return ``True`` if ``rarity`` is considered high-tier."""

    return int(rarity) >= int(HIGH_RARITY_THRESHOLD)


def notify_high_rarity_drop(player, item, position):
    """Send a notification about a high-rarity ``item`` to ``player``.

    Parameters
    ----------
    player : :class:`game.player.Player` or ``None``
        Recipient of the message. ``None`` is silently ignored.
    item : :class:`game.item.Item`
        The item that was dropped.
    position : :class:`game.position.Position`
        Where the visual effect should appear.
    """

    if not player or not is_high_rarity(item.rarity):
        return

    rarity_name = RARITY_CONFIG[item.rarity]["name"]
    msg = HIGH_RARITY_MESSAGE.format(rarity=rarity_name, item=item.rawName())
    player.message(msg, game.const.MSG_INFO_DESCR)
    player.magicEffect(HIGH_RARITY_EFFECT, position)
