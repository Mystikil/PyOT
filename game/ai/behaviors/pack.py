"""Behavior for pack hunting monsters."""

from ..core import Behavior
from game.functions import getCreatures
from game import monster as monster_module


class PackAI(Behavior):
    """Causes nearby monsters of the same type to assist when aggroing."""

    def __init__(self, monster, radius=6):
        super().__init__(monster)
        self.radius = radius

    def on_aggro(self, target):
        for creature in getCreatures(self.monster.position, (self.radius, self.radius)):
            if creature is self.monster:
                continue
            if isinstance(creature, monster_module.Monster) and creature.base == self.monster.base:
                if not creature.target:
                    creature.target = target
                    creature.targetMode = 1
                    if hasattr(creature, "ai") and creature.ai:
                        creature.ai.on_aggro(target)
