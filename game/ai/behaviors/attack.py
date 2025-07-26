from ..core import Behavior
from data.scripts.other.monsterbrain import defaultBrainFeature

class AttackAI(Behavior):
    """Behavior that executes the default attack logic."""
    def on_think(self):
        return defaultBrainFeature(self.monster)

