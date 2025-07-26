@register('talkactionFirstWord', '!report')
def report_issue(creature, text):
    if not text:
        creature.lmessage("You must provide a report message.")
        return False
    import datetime
    import config
    from game.item import Item
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"logs/Error.{creature.name()}.{now}.txt"
    try:
        with open(filename, 'w') as fh:
            fh.write(text.strip())
    except Exception:
        creature.lmessage("Could not save your report.")
        return False
    try:
        reward_id = getattr(config, 'reportRewardItemId', 2160)
        creature.addItem(Item(reward_id))
    except Exception:
        pass
    creature.lmessage('Thank you for the report.')
    return False

