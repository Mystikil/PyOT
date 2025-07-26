@register("talkaction", "/remove")
@access("DEVELOPER")
def remove_thing(creature, text):
    position = creature.positionInDirection(creature.direction)
    tile = game.map.getTile(position)

    if not tile:
        creature.lmessage("Object not found.")
        return False

    thing = tile.getTopVisibleThing(creature)

    if not thing:
        creature.lmessage("Thing not found.")
        return False

    if thing.isCreature():
        thing.remove()
    elif thing.isItem():
        if thing == tile.getGround():
            creature.lmessage("You may not remove a ground tile.")
            return False
        count = int(text) if text.isdigit() else -1
        thing.remove(count)

    creature.magicEffect(EFFECT_MAGIC_RED, position)
    return False
