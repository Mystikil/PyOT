@register("talkaction", "/invisible")
@access("INVISIBLE")
def invisible(creature, text):
    creature.condition(Condition(CONDITION_INVISIBLE, length=30))
    creature.broadcast(f"{creature.name()} is now invisible.")
    return False
