"""Basic combat utilities emulating TFS style damage calculations."""

import random


def calculate_damage(min_damage, max_damage, crit_chance=0.0, crit_multiplier=1.5):
    """Return (damage, crit) applying random and critical hit logic."""
    dmg = random.randint(min_damage, max_damage)
    crit = False
    if crit_chance and random.random() <= crit_chance:
        dmg = int(dmg * crit_multiplier)
        crit = True
    return dmg, crit


def perform_attack(attacker, target, *, min_damage, max_damage, dmg_type,
                    crit_chance=0.0, crit_multiplier=1.5,
                    effect=None, projectile=None):
    """Apply damage and visual effects between ``attacker`` and ``target``."""
    dmg, crit = calculate_damage(min_damage, max_damage, crit_chance, crit_multiplier)

    if projectile and hasattr(attacker, "send_magic_effect"):
        attacker.send_magic_effect(attacker.position, projectile)

    if effect and hasattr(target, "send_magic_effect"):
        target.send_magic_effect(target.position, effect)

    if hasattr(target, "deal_damage"):
        target.deal_damage(dmg, dmg_type)

    return dmg, crit

