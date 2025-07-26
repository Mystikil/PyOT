@register("talkaction", "/clean")
@access("MANAGESERVER")
def clean_map_command(creature, text):
    count = clean_map()
    if count:
        creature.message(f"Cleaned {count} item{'s' if count != 1 else ''} from the map.")
    return False


def clean_map():
    removed = 0
    for pos_sum, tile in list(game.map.knownMap.items()):
        items_to_remove = [item for item in tile.getItems() if item.pickable]
        for item in items_to_remove:
            try:
                item.remove()
                removed += 1
            except Exception:
                pass
    return removed