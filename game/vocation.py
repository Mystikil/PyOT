"""Vocation handling utilities.

This module provides a simple registration system for vocations as
well as the :class:`Vocation` class described in the documentation.
"""

from typing import Callable, Dict, Optional

__all__ = [
    "Vocation",
    "regVocation",
    "getVocation",
    "getVocationById",
]

# Internal mappings of registered vocations
_vocations_by_id: Dict[int, "Vocation"] = {}
_vocations_by_name: Dict[str, "Vocation"] = {}
_vocations_by_cid: Dict[int, "Vocation"] = {}


class Vocation(object):
    """Representation of a vocation type."""

    def __init__(self, id: int, cid: int, name: str, description: str,
                 health: int, mana: int, soulticks: int) -> None:
        self.id = id
        self.cid = cid
        self.name = name
        self._description = description
        self.base_health = health
        self.base_mana = mana
        self.soulticks = soulticks

        # formula/constant placeholders
        self._cap_formula: Callable[[int], int] = lambda lvl: 0
        self._hp_formula: Callable[[int], int] = lambda lvl: health
        self._mana_formula: Callable[[int], int] = lambda lvl: mana
        self.meleeSkill = 1
        self.mlevel = 1
        self._max_soul = 0

    # ------------------------------------------------------------------
    # configuration helpers used by scripts
    # ------------------------------------------------------------------
    def capacityFormula(self, formula: Callable[[int], int]) -> None:
        """Set the capacity formula used by :meth:`maxCapacity`."""
        self._cap_formula = formula

    def hpFormula(self, formula: Callable[[int], int]) -> None:
        """Set the maximum health formula used by :meth:`maxHP`."""
        self._hp_formula = formula

    def manaFormula(self, formula: Callable[[int], int]) -> None:
        """Set the maximum mana formula used by :meth:`maxMana`."""
        self._mana_formula = formula

    def meleeSkillConstant(self, constant: int) -> None:
        """Set the melee skill constant."""
        self.meleeSkill = constant

    def mlevelConstant(self, constant: int) -> None:
        """Set the magic level constant."""
        self.mlevel = constant

    def maxSoul(self, soul: int) -> None:
        """Set the maximum soul amount."""
        self._max_soul = soul

    # ------------------------------------------------------------------
    # accessors
    # ------------------------------------------------------------------
    def description(self) -> str:
        """Return the vocation description."""
        return self._description

    def maxCapacity(self, level: int) -> int:
        """Return maximum capacity for ``level``."""
        return self._cap_formula(level)

    def maxHP(self, level: int) -> int:
        """Return maximum health for ``level``."""
        return self._hp_formula(level)

    def maxMana(self, level: int) -> int:
        """Return maximum mana for ``level``."""
        return self._mana_formula(level)



# ----------------------------------------------------------------------
# Registration helpers
# ----------------------------------------------------------------------

def regVocation(id: int, cid: int, name: str, description: str,
                health: int, mana: int, soulticks: int) -> Vocation:
    """Register a new vocation and return the :class:`Vocation` object."""
    voc = Vocation(id, cid, name, description, health, mana, soulticks)
    _vocations_by_id[id] = voc
    _vocations_by_name[name] = voc
    _vocations_by_cid[cid] = voc
    return voc


def getVocation(name: str) -> Optional[Vocation]:
    """Get a vocation by ``name``."""
    return _vocations_by_name.get(name)


def getVocationById(id: int) -> Optional[Vocation]:
    """Get a vocation by ``id``."""
    return _vocations_by_id.get(id)
