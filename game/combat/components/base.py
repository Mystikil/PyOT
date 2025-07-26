from ..context import CombatContext


class CombatComponent:
    """Base class for combat resolution components."""

    def apply(self, context: CombatContext):
        """Apply this component to the context."""
        raise NotImplementedError("Component must implement apply()")
