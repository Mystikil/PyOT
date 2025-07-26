# Changelog

## Unreleased
- Website news editor now supports rich formatting via TinyMCE. Run
  `ALTER TABLE news MODIFY body MEDIUMTEXT NOT NULL;` to expand stored content.
- Enforced client specific item id limits in protocol layer and added fallback
  item replacements for unsupported item ids.
- Added max magic effect id handling so unsupported effects fall back to
  ``EFFECT_POFF`` instead of crashing older clients.
- Added player notification and firework effect for loot items of
  `CELESTIUM_CLASS` rarity or higher.
- Introduced `rarity_exclusions.json` to disable random rarity on specific items.
- Fixed login crashes when custom `magicLevelFromManaFormula` expected two
  parameters. Player initialization now tries both signatures to avoid errors.
- Servers now exit with a clear error message when their configured port is
  already in use instead of crashing with a traceback.
- Added `FleeAI` behavior and made monsters fall back to `AttackAI` when no
  behaviors are specified, ensuring legacy behaviour remains unchanged.
- Implemented dynamic monster ranks that randomly promote spawned monsters
  to Elite, Champion, Boss or Overlord variants with scaled stats.
- Fixed indentation in `MonsterBase.spawn` which caused SyntaxError on some
  Windows setups.
- Resolved incorrect descriptions when looking at walls or other fixed objects.

