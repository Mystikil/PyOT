classes = {'red': MSG_STATUS_CONSOLE_RED,
           'white': MSG_EVENT_ADVANCE,
           'green': MSG_INFO_DESCR,
           'warning': MSG_STATUS_WARNING}

@register("talkactionFirstWord", "/B")
@access("TALK_RED")
def broadcastMessageUpper(creature, text):
    msgclass = MSG_STATUS_WARNING
    msgcolor = 'warning'
    if not text or text.count(';') > 1:
        return False

    parts = text.split(';')
    if len(parts) == 2:
        msg, msgcolor = parts
    else:
        msg = text

    try:
        msgclass = classes[msgcolor.lower().strip()]
    except Exception:
        pass

    for name in game.player.allPlayers:
        player = game.player.allPlayers[name]
        if player.alive and player.client.ready:
            player.message(f"{creature.name()}: {msg}", msgclass)
    return False
