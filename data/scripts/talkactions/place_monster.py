@register("talkactionFirstWord", "/m")
@access("SPAWN")
def placeMonster(creature, text):
    if not text:
        creature.lmessage("Monster name required.")
        return False

    pos = creature.position.copy()
    pos.y += 1
    try:
        game.monster.getMonster(text.title()).spawn(pos)
    except Exception:
        creature.lmessage("Monster named '%s' can't be spawned!" % text)
    return False
