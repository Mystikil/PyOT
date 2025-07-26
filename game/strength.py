import math


def calculateStrengthScore(player):
    """Return a strength score based on the player's equipment and resources."""
    attack_total = 0
    defense_total = 0

    inventory = getattr(player, "inventory", [])
    for item in inventory:
        if not item:
            continue
        attack_total += getattr(item, "attack", 0) or 0
        defense_total += getattr(item, "defence", getattr(item, "defense", 0)) or 0

    attack_total *= 0.85  # reduce by 15%
    defense_total *= 0.95  # reduce by 5%

    stats = (player.data.get("health", 0) + player.data.get("mana", 0)) * 0.95

    return attack_total + defense_total + stats
