"""Teleport utilities fixing movement lock issues."""

import time

from .map import getTile
from .errors import SolidTile


def teleport_player(player, position, force=False):
    """Safely teleport ``player`` to ``position``.

    This helper clears queued movement, validates the target tile and then
    calls ``player.teleport``. It ensures the client is correctly updated
    afterwards.
    """

    # 1. Cancel movement and queued actions
    if hasattr(player, "stopAction"):
        try:
            player.stopAction()
        except Exception:
            pass
    if hasattr(player, "cancelWalk"):
        try:
            player.cancelWalk()
        except Exception:
            pass
    if hasattr(player, "lastClientMove"):
        player.lastClientMove = None
    if hasattr(player, "walkPattern"):
        player.walkPattern = None

    # 2. Validate destination
    tile = getTile(position)
    if not tile:
        raise SolidTile("Tile doesn't exist")
    if not force:
        for item in tile.getItems():
            if getattr(item, "solid", False):
                raise SolidTile()

    # 3. Reset movement timing
    now = time.time()
    if hasattr(player, "lastAction"):
        player.lastAction = now
    if hasattr(player, "lastStairHop"):
        player.lastStairHop = now

    # 4. Use built in teleport and refresh
    if hasattr(player, "teleport"):
        player.teleport(position, force)
    else:
        player.position = position
        if hasattr(player, "refreshViewWindow"):
            player.refreshViewWindow()
        if hasattr(player, "send_map_update"):
            player.send_map_update()
