@register("talkactionFirstWord", '/i')
@access("CREATEITEM")
def makeitem(creature, text):
    """Create items by id or name.

    Examples
    --------
    /i 2160, 100
    /i crystal coin, 100
    /i 3043
    """

    try:
        name_part = text
        count = 1

        if ',' in text:
            name_part, count_text = text.split(',', 1)
            count_text = count_text.strip()
            if count_text:
                count = int(count_text)

        name_part = name_part.strip()

        # Support old syntax: "/i <id> <count>"
        if ' ' in name_part and name_part.split(' ')[1].isdigit():
            parts = name_part.split(' ', 1)
            name_part = parts[0]
            count = int(parts[1])

        # Determine the item id from either a numeric id or a name
        if name_part.isdigit():
            itemid = int(name_part)
        else:
            itemid = game.item.idByName(name_part)

        if not itemid:
            creature.message("Invalid Item!")
            return False

        while count:
            rcount = min(100, count)
            newitem = Item(itemid, rcount)
            if newitem.pickable:
                creature.addItem(newitem)
            else:
                newitem.place(creature.position)

            count -= rcount

        creature.magicEffect(EFFECT_MAGIC_GREEN)

    except Exception:
        creature.message("Invalid Item!")

    return False


# Create item by name ex: /in magic longsword, 1

@register("talkactionFirstWord", '/in')
@access("CREATEITEM")
def createItemByName(creature, text):
    """Backward compatible alias for `/i <item name>, <count>`."""
    return makeitem(creature, text)
