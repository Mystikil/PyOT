# Item Rarity System

This document explains the monster loot rarity system.

## Overview

Items dropped by monsters can now receive a random rarity. Each rarity tier defines a multiplier for the item's combat stats and an independent chance to appear.

Rarity data is stored in `game/rarity.py` as `RARITY_CONFIG` together with an enumeration `Rarity`.

## Rarity Levels

The game supports seventeen tiers listed below.

| Value | Name | Multiplier | Drop Chance |
|-------|------|------------|-------------|
| 0 | Junk | 1.0 | 0.4 |
| 1 | Uncommon | 1.05 | 0.25 |
| 2 | Common | 1.1 | 0.15 |
| 3 | Rare | 1.2 | 0.08 |
| 4 | Epic | 1.3 | 0.05 |
| 5 | Legendary | 1.45 | 0.03 |
| 6 | Master Crafted | 1.6 | 0.015 |
| 7 | Mythforged | 1.75 | 0.01 |
| 8 | Eclipseborn | 1.9 | 0.007 |
| 9 | Dreadnaught Relic | 2.05 | 0.004 |
| 10 | Celestium-Class | 2.2 | 0.003 |
| 11 | Wyrmshadow | 2.4 | 0.002 |
| 12 | Oblivion-Touched | 2.6 | 0.0015 |
| 13 | Ashen King's Legacy | 2.8 | 0.001 |
| 14 | Veilpiercer | 3.0 | 0.0007 |
| 15 | Primordial Sigil | 3.5 | 0.0004 |
| 16 | Godrend | 4.0 | 0.0002 |

The `multiplier` scales the item's `attack`, `defense` and `armor` values when the rarity is applied. `dropChance` defines how likely it is for an item to receive the corresponding rarity.

## Applying Rarity

`game.rarity.apply_rarity_to_item(item)` performs the following steps:

1. Randomly selects a rarity using the weighted chances above.
2. Stores the rarity identifier on the item (`item.rarity`).
3. Generates a serial number. The rarity text is stored on the item as
   `item.rarity_description` while the serial itself is kept separately as
   `item.rarity_serial`.
4. Scales combat stats by the configured multiplier.

A helper `assign_rarity()` is provided if you only need the rarity value.

## Integration with Monster Loot

When a monster dies, each item spawned in its corpse runs `apply_rarity_to_item` before being placed. The base loot table remains untouched, so existing drop rates are unaffected. Only the item's stats and description are modified at creation time.

## Extending

Edit `game/rarity.py` to tweak multipliers or drop chances. New rarities can be added by expanding the `Rarity` enum and `RARITY_CONFIG` dictionary.

## High-Rarity Notifications

Rarities at or above `CELESTIUM_CLASS` (value `10`) trigger a special message
and visual effect when dropped. The constants controlling this behaviour are
defined in `game/rarity.py`:

```
HIGH_RARITY_THRESHOLD = Rarity.CELESTIUM_CLASS
HIGH_RARITY_EFFECT = game.const.EFFECT_FIREWORK_BLUE
HIGH_RARITY_MESSAGE = "🔥 You looted a {rarity} {item}!"
```

To change the threshold or effect, edit these values. The function
`notify_high_rarity_drop(player, item, position)` handles displaying the message
and magic effect.

## Excluding Items from Random Rarity

The file `data/rarity_exclusions.json` contains a JSON array of item IDs. Any
item whose ID appears in this list will bypass the rarity system when dropped.
For example:

```
[1001, 1002, 1003]
```

Items listed here are left unchanged when `apply_rarity_to_item` is invoked.
