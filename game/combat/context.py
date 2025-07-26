from typing import Optional, List


class CombatContext:
    """Context information passed through combat resolution."""

    def __init__(self, attacker, target, weapon: Optional[object] = None,
                 spell: Optional[object] = None, area: Optional[object] = None):
        self.attacker = attacker
        self.target = target
        self.weapon = weapon
        self.spell = spell
        self.area = area
        self.damage = 0
        self.critical = False
        self.hit = True
        self.miss_reason: Optional[str] = None
        self.log: List[str] = []
        self.tags = set()
        self.conditions_to_apply: List[object] = []

    def add_log(self, entry: str):
        self.log.append(entry)
