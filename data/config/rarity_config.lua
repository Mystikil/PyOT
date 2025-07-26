-- Rarity configuration file
RARITY_CONFIG = {
  [1] = {name = "Junk", multiplier = 0.5, dropChance = 0.25, effect = CONST_ME_POFF},
  [2] = {name = "Uncommon", multiplier = 0.75, dropChance = 0.2, effect = CONST_ME_BLOCKHIT},
  [3] = {name = "Common", multiplier = 1.0, dropChance = 0.15, effect = CONST_ME_HITAREA},
  [4] = {name = "Rare", multiplier = 1.25, dropChance = 0.1, effect = CONST_ME_MAGIC_GREEN},
  [5] = {name = "Epic", multiplier = 1.5, dropChance = 0.07, effect = CONST_ME_MAGIC_RED},
  [6] = {name = "Legendary", multiplier = 1.75, dropChance = 0.05, effect = CONST_ME_FIREWORK_RED},
  [7] = {name = "Master Crafted", multiplier = 2.0, dropChance = 0.035, effect = CONST_ME_FIREWORK_YELLOW},
  [8] = {name = "Mythforged", multiplier = 2.25, dropChance = 0.025, effect = CONST_ME_ENERGYHIT},
  [9] = {name = "Eclipseborn", multiplier = 2.5, dropChance = 0.02, effect = CONST_ME_MORTAREA},
  [10] = {name = "Dreadnaught Relic", multiplier = 2.75, dropChance = 0.015, effect = CONST_ME_GIANTICE},
  [11] = {name = "Celestium-Class", multiplier = 3.0, dropChance = 0.01, effect = CONST_ME_GROUNDSHAKER},
  [12] = {name = "Wyrmshadow", multiplier = 3.5, dropChance = 0.007, effect = CONST_ME_PURPLEENERGY},
  [13] = {name = "Oblivion-Touched", multiplier = 4.0, dropChance = 0.005, effect = CONST_ME_TELEPORT},
  [14] = {name = "Ashen King’s Legacy", multiplier = 4.5, dropChance = 0.003, effect = CONST_ME_FIREAREA},
  [15] = {name = "Veilpiercer", multiplier = 5.0, dropChance = 0.002, effect = CONST_ME_BUBBLES},
  [16] = {name = "Primordial Sigil", multiplier = 6.0, dropChance = 0.001, effect = CONST_ME_SOUND_RED},
  [17] = {name = "Godrend", multiplier = 7.5, dropChance = 0.0005, effect = CONST_ME_GIFT_WRAPS},
}

BROADCAST_RARITY_THRESHOLD = 13  -- Broadcast drop if rarity >= this value
