# Modular Monster AI

This folder implements a modular AI system for monsters. Instead of a single monolithic
script controlling each creature, monsters can compose multiple **behaviors** which are
managed by a central `MonsterAI` object. Behaviors handle events such as thinking,
target acquisition, damage and death.

## Core Classes

The entry point is [`game/ai/core.py`](core.py) which defines two classes:

```python
class Behavior:
    """Base class for AI behavior modules."""
    def on_think(self):
        pass
    def on_aggro(self, target):
        pass
    def on_damage(self, attacker, amount, damage_type):
        pass
    def on_death(self):
        pass
```

```python
class MonsterAI:
    """AI manager that dispatches events to registered behaviors."""
    def __init__(self, monster, behaviors: Iterable[Type[Behavior]] = None):
        ...
    def add_behavior(self, behavior):
        ...
    def on_think(self):
        ...
    def on_aggro(self, target):
        ...
    def on_damage(self, attacker, amount, damage_type):
        ...
    def on_death(self):
        ...
```

`MonsterAI` holds a list of behavior objects and forwards lifecycle events to each
one. Exceptions raised inside behaviors are caught so that the main game loop is not
interrupted.

## Behavior Lifecycle

Behavior modules may implement any of the following hooks:

- **`on_think()`** – called every AI tick from the monster think loop.
- **`on_aggro(target)`** – invoked when the monster first selects a target.
- **`on_damage(attacker, amount, damage_type)`** – triggered whenever the monster
  takes damage.
- **`on_death()`** – run right before the monster dies.

Implement only the hooks you need; the defaults in `Behavior` are no-ops.

## Registering Behaviors

A monster base registers the behaviors it wants via the [`ai()` method in
`game/monster.py`](../monster.py):

```python
    def ai(self, *modules):
        """Register AI behavior modules for monsters spawned from this base."""
        self.ai_modules = modules
        return self
```

When a monster is spawned, a [`MonsterAI`](core.py) instance is created with the
configured modules:

```python
monster = Monster(self, position, None)
if not self.prepared:
    self.prepare()
from game.ai import MonsterAI
monster.ai = MonsterAI(monster, self.ai_modules)
```

During the think loop, the AI is invoked instead of the legacy brain features:

```python
if hasattr(monster, "ai") and monster.ai:
    ret = monster.ai.on_think()
else:
    ret = brainFeatures[monster.base.brainFeatures](monster)
```

## Built‑in Behaviors

Several behavior classes ship with the system under [`game/ai/behaviors`](behaviors):

- **`PackAI`** – nearby monsters of the same type assist when one aggroes.
- **`RangedAI`** – keeps the monster at a distance from its target.
- **`HunterAI`** – simple alias for `RangedAI` used by ranged hunters.
- **`AttackAI`** – runs the default attack logic defined in
  `data.scripts.other.monsterbrain`.
- **`FleeAI`** – makes the monster retreat when low on health.

Import them from `game.ai.behaviors` when assigning AI modules.

If a monster does not specify any behaviors via `ai()`, it automatically gets
`AttackAI` so existing monsters keep their classic behaviour.

## Example Usage

The wolf monster demonstrates composition of multiple behaviors
([`data/monsters/Mammals/Canines/Wolf.py`](../../data/monsters/Mammals/Canines/Wolf.py)):

```python
from game.ai.behaviors.pack import PackAI
from game.ai.behaviors.hunter import HunterAI
from game.ai.behaviors.attack import AttackAI
Wolf.ai(PackAI, HunterAI, AttackAI)
```

With this configuration, wolves call nearby pack members when aggroing, maintain
ranged distance while hunting and perform the default attack logic each tick.

## Creating Custom Behaviors

To extend the system, create a subclass of `Behavior` and override any hooks you
need. The constructor receives the monster instance so you can access its state:

```python
from game.ai.core import Behavior

class FleeAI(Behavior):
    def __init__(self, monster, threshold=0.3):
        super().__init__(monster)
        self.threshold = threshold

    def on_think(self):
        if self.monster.healthPercent() < self.threshold:
            self.monster.runAway()
```

Register your custom behavior together with the provided ones when defining the
monster base.

## Summary

The modular AI framework lets monsters mix and match small, focused behaviors.
`MonsterAI` coordinates these modules and forwards events from the existing game
loop. This approach simplifies customization and encourages reusable AI logic
across different monster types.
