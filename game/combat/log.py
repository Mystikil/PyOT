class BattleLog:
    """Simple collector for combat log entries."""

    def __init__(self):
        self.entries = []

    def add(self, entry: str):
        self.entries.append(entry)

    def display(self) -> str:
        return "\n".join(self.entries)
