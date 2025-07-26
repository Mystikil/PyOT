# Extended Feature Guide

This document explains the new rarity system, equipment set bonuses, and the item serialization interface.

## Rarity System

Item rarity is defined by the `Rarity` enumeration in `game/rarity.py` which lists 17 discrete levels ranging from `JUNK` to `GODREND`:

```
from enum import IntEnum

class Rarity(IntEnum):
    """Enumeration of item rarity levels."""

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
```

Each item can have a `"rarity"` field in `data/items.json`. When items are loaded, `_applyRarityMultipliers` from `game/item.py` adjusts various numeric stats based on a configurable multiplier:

```
mult = config.rarityStatMultipliers.get(item.get("rarity", Rarity.JUNK), 1.0)
...
stat_keys = (
    "armor", "attack", "defense", "extraatk", "extradef",
    "magiclevelpoints", "magicpoints",
    "skillFist", "skillClub", "skillSword", "skillAxe",
    "skillDist", "skillShield",
    "hitChance", "maxHitChance", "healthGain", "manaGain",
    "elementPhysical", "elementFire", "elementIce",
    "elementEarth", "elementDeath", "elementEnergy",
    "elementHoly", "elementDrown",
    "absorbPercentAll", "absorbPercentPhysical",
    "absorbPercentFire", "absorbPercentIce",
    "absorbPercentEarth", "absorbPercentEnergy",
    "absorbPercentHoly", "absorbPercentDrown",
    "absorbPercentDeath", "absorbPercentPoison",
    "absorbPercentManaDrain", "absorbPercentLifeDrain",
)
```

Multipliers per rarity are defined in `config.py.dist` as `rarityStatMultipliers`. Example configuration:

```
from game.rarity import Rarity

rarityStatMultipliers = {
    Rarity.JUNK.value: 1.0,
    Rarity.UNCOMMON.value: 1.05,
    Rarity.COMMON.value: 1.10,
    Rarity.RARE.value: 1.20,
}
```

### Using Rarity

1. Edit `config.py` and adjust `rarityStatMultipliers`.
2. Tag items in `data/items.json` with a `"rarity"` integer.
3. Reload items with `game.item.loadItems()`.

## Equipment Set Bonuses

Equipment sets allow granting bonuses when a player equips several matching pieces. Set names are specified per item, for example in `data/items.json`:

```
{
    "id": 2493,
    "cid": 3387,
    "name": "demon helmet",
    "setName": "demon",
    ...
}
```

Bonuses per set are configured in `userconfig.py` under `equipmentSetBonuses`:

```
equipmentSetBonuses = {
    "demon": {
        2: {"healthmax": 50},
        3: {"healthmax": 100},
        4: {"healthmax": 150}
    }
}
```

The script `data/scripts/other/set_bonuses.py` hooks into equip and unequip events using `registerForAttr`:

```
registerForAttr('equip', 'setName', on_equip)
registerForAttr('unequip', 'setName', on_unequip)
```

When the player equips or removes an item with a `setName`, `_update_set` applies or removes a long-duration `Boost` condition as pieces are collected. Active bonuses are tracked in `player.activeSetBonuses`.

### Using Set Bonuses

1. Add `setName` fields to items you want grouped in a set.
2. Define stat bonuses for that set in `userconfig.py` under `equipmentSetBonuses`.
3. Ensure `data/scripts/other/set_bonuses.py` is loaded by the script system.

## Item Serialization

Individual items can be stored persistently using unique serial numbers. Each `Item` instance is assigned a UUID on creation and implements `__getstate__`/`__setstate__` for pickling. The table schema is defined in `extra/sql/2000_item_serials.sql`:

```
CREATE TABLE IF NOT EXISTS `items` (
  `serial` varchar(32) NOT NULL,
  `data` mediumblob NOT NULL,
  PRIMARY KEY (`serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

Helper functions in `game/item.py` provide save/load routines:

```
@gen.coroutine
def saveItem(item):
    data = pickle.dumps(item, 3)
    yield sql.runOperation(
        "REPLACE INTO items(`serial`, `data`) VALUES(%s, %s)", item.serial, data
    )

@gen.coroutine
def loadItem(serial):
    result = yield sql.runQuery("SELECT `data` FROM items WHERE `serial`=%s", serial)
    if not result:
        raise gen.Return(None)
    item = pickle.loads(result[0]["data"])
    raise gen.Return(item)
```

### Using Serialization

1. Apply the SQL update `extra/sql/2000_item_serials.sql` to create the `items` table.
2. Call `saveItem(item)` to store any `Item` instance.
3. Retrieve it later with `loadItem(serial)`.

This allows long-term persistence of unique items across server restarts or transfers.

### Market Integration

Market offers now store an optional `item_serial` field. When a player lists a unique
item for sale the item instance is serialized and removed from their depot. Buyers
receive the exact item when purchasing and the entry is deleted from the `items`
table once delivered or when an offer expires.

### Admin Item Lookup

The web admin panel has a new "Lookup Item" section. Administrators may search for
an item by serial and duplicate the stored record if necessary.

