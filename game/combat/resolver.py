from typing import List

from .context import CombatContext
from .components.base import CombatComponent


class CombatResolver:
    """Applies a series of components to a combat context."""

    def __init__(self, components: List[CombatComponent]):
        self.components = components

    def resolve(self, context: CombatContext) -> CombatContext:
        for comp in self.components:
            comp.apply(context)
            if not context.hit:
                break
        return context
