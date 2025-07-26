"""Modular combat system package."""

from .context import CombatContext
from .resolver import CombatResolver
from .condition import Condition
from .log import BattleLog
from .tags import CombatTag

# Components subpackage
from .components.base import CombatComponent
from .components.standard import (
    BaseDamageComponent,
    CriticalHitComponent,
    ResistanceComponent,
    HitChanceComponent,
)

__all__ = [
    'CombatContext',
    'CombatResolver',
    'Condition',
    'BattleLog',
    'CombatTag',
    'CombatComponent',
    'BaseDamageComponent',
    'CriticalHitComponent',
    'ResistanceComponent',
    'HitChanceComponent',
]
