@register('talkaction', '!stuck')
def stuck(creature, **k):
    import data.map.info
    x, y, z = data.map.info.towns[creature.data['town_id']][1]
    try:
        creature.teleport(Position(x, y, z))
    except Exception:
        creature.lmessage("You can't go there!")
    else:
        creature.magicEffect(EFFECT_TELEPORT)
    return False
