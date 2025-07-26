class Condition:
    """Simple condition that can be applied to targets."""

    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration

    def apply(self, target):
        target.add_condition(self)

    def tick(self, target):
        self.duration -= 1
        if self.duration <= 0:
            self.expire(target)

    def expire(self, target):
        target.remove_condition(self)
