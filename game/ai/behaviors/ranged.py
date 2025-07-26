"""Ranged combat behavior keeping distance from the target."""

from ..core import Behavior


class RangedAI(Behavior):
    """Simple ranged AI that tries to maintain a safe distance."""

    def __init__(self, monster, min_range=3, max_range=5):
        super().__init__(monster)
        self.min_range = min_range
        self.max_range = max_range

    def on_think(self):
        m = self.monster
        if not m.target:
            return

        dist = m.distanceStepsTo(m.target.position)
        if dist < self.min_range and not m.walkPattern:
            dx = m.position.x - m.target.position.x
            dy = m.position.y - m.target.position.y
            if abs(dx) > abs(dy):
                direction = 1 if dx > 0 else 3
            else:
                direction = 0 if dy > 0 else 2
            m.move(direction, stopIfLock=True, push=False)
        elif dist > self.max_range and not m.walkPattern:
            m.walk_to(m.target.position, -self.max_range, lambda x: m.turnAgainst(m.target.position))
