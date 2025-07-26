from ..core import Behavior

class FleeAI(Behavior):
    """Run away from the target when below a health threshold."""

    def __init__(self, monster, threshold=0.3):
        super().__init__(monster)
        self.threshold = threshold

    def on_think(self):
        m = self.monster
        if not m.target:
            return
        if m.data.get("healthmax") and m.data["health"]/m.data["healthmax"] <= self.threshold:
            dx = m.position.x - m.target.position.x
            dy = m.position.y - m.target.position.y
            if abs(dx) > abs(dy):
                direction = 1 if dx > 0 else 3
            else:
                direction = 0 if dy > 0 else 2
            m.move(direction, stopIfLock=True, push=False)
