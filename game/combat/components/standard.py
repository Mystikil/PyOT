import random
from .base import CombatComponent
from ..context import CombatContext


class BaseDamageComponent(CombatComponent):
    def __init__(self, min_dmg: int, max_dmg: int):
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def apply(self, context: CombatContext):
        context.damage = random.randint(self.min_dmg, self.max_dmg)
        context.add_log(f"Base damage rolled: {context.damage}")


class CriticalHitComponent(CombatComponent):
    def __init__(self, chance: float = 0.1, multiplier: float = 2.0):
        self.chance = chance
        self.multiplier = multiplier

    def apply(self, context: CombatContext):
        if random.random() <= self.chance:
            context.damage = int(context.damage * self.multiplier)
            context.critical = True
            context.add_log("Critical hit!")


class ResistanceComponent(CombatComponent):
    def __init__(self, dtype: str = 'physical'):
        self.dtype = dtype

    def apply(self, context: CombatContext):
        if not hasattr(context.target, 'get_resistance'):
            return
        resist = context.target.get_resistance(self.dtype)
        reduced = int(context.damage * (1 - resist))
        context.add_log(f"{self.dtype.title()} resistance applied: {context.damage} -> {reduced}")
        context.damage = reduced


class HitChanceComponent(CombatComponent):
    def __init__(self, accuracy: float):
        self.accuracy = accuracy

    def apply(self, context: CombatContext):
        if random.random() > self.accuracy:
            context.hit = False
            context.miss_reason = "Missed"
            context.add_log("Attack missed!")
