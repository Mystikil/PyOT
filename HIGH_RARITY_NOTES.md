# High-Rarity Drop Notifications

This document describes the implementation of special notifications when a monster drops high-tier loot.

## Modified Files
- `game/rarity.py` – added constants and helper functions for high-rarity detection and notifications.
- `game/monster.py` – calls `notify_high_rarity_drop` when placing loot.
- `RARITY_SYSTEM.md` – documented the configuration values.

## Behaviour
When an item with rarity `HIGH_RARITY_THRESHOLD` or higher is generated in a monster's loot, the killer receives a chat message and a firework effect plays at the corpse's position. The rarity is determined when `apply_rarity_to_item` is called.

## Customization
Edit the constants in `game/rarity.py` to change which rarities trigger the effect, which magic effect ID is used, or to alter the message text. The function `notify_high_rarity_drop` can also be reused by other game systems if needed.
