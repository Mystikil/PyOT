@register("talkaction", "/attr")
@access("DEVELOPER")
def set_attribute(creature, text):
    if ',' not in text:
        creature.lmessage("Usage: /attr attribute, value")
        return False

    attr_name, value = map(str.strip, text.split(',', 1))
    pos = creature.positionInDirection(creature.direction)
    tile = game.map.getTile(pos)

    if not tile:
        creature.lmessage("There is no tile in front of you.")
        return False

    thing = tile.getTopVisibleThing(creature)
    if not thing:
        creature.lmessage("There is an empty tile in front of you.")
        return False

    if not thing.isItem():
        creature.lmessage("Thing in front of you is not an item.")
        return False

    try:
        thing.setAttribute(attr_name, value)
        attr_value = thing.getAttribute(attr_name)
        creature.lmessage(f"Attribute '{attr_name}' set to: {attr_value}")
        creature.magicEffect(EFFECT_MAGIC_GREEN, pos)
    except Exception as e:
        creature.lmessage(f"Error setting attribute: {e}")

    return False
