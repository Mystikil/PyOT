"""Simple event system for Python scripts."""

from collections import defaultdict


_event_handlers = defaultdict(list)


def register_event(event_type, handler):
    """Register a new ``handler`` for ``event_type``."""
    _event_handlers[event_type].append(handler)


def emit_event(event_type, **kwargs):
    """Emit an event and pass ``kwargs`` to handlers.

    If a handler returns ``False`` the processing chain stops.
    """
    for handler in list(_event_handlers.get(event_type, [])):
        result = handler(**kwargs)
        if result is False:
            break

