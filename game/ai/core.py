"""Core classes for the Monster AI framework."""

from typing import Iterable, Type


class Behavior:
    """Base class for AI behavior modules."""

    def __init__(self, monster):
        self.monster = monster

    # Lifecycle hooks -----------------------------------------------------
    def on_think(self):
        """Called periodically from the monster think loop."""
        pass

    def on_aggro(self, target):
        """Called when the monster acquires a target."""
        pass

    def on_damage(self, attacker, amount, damage_type):
        """Called whenever the monster takes damage."""
        pass

    def on_death(self):
        """Called when the monster dies."""
        pass


class MonsterAI:
    """AI manager that dispatches events to registered behaviors."""

    def __init__(self, monster, behaviors: Iterable[Type[Behavior]] = None):
        self.monster = monster
        self.behaviors = []
        if behaviors:
            for beh in behaviors:
                self.add_behavior(beh)

    def add_behavior(self, behavior):
        if isinstance(behavior, type):
            behavior = behavior(self.monster)
        self.behaviors.append(behavior)

    # Dispatch helpers ----------------------------------------------------
    def on_think(self):
        for beh in self.behaviors:
            try:
                beh.on_think()
            except Exception:
                # Behaviors should never crash the main loop
                from .. import scriptsystem
                scriptsystem.handle_script_exception()
        return None

    def on_aggro(self, target):
        for beh in self.behaviors:
            try:
                beh.on_aggro(target)
            except Exception:
                from .. import scriptsystem
                scriptsystem.handle_script_exception()

    def on_damage(self, attacker, amount, damage_type):
        for beh in self.behaviors:
            try:
                beh.on_damage(attacker, amount, damage_type)
            except Exception:
                from .. import scriptsystem
                scriptsystem.handle_script_exception()

    def on_death(self):
        for beh in self.behaviors:
            try:
                beh.on_death()
            except Exception:
                from .. import scriptsystem
                scriptsystem.handle_script_exception()
