from game.conditions import Boost
from game.const import CONDITION_BUFF, CONDITION_REPLACE
from game.scriptsystem import registerForAttr
import userconfig


def on_equip(creature, thing, slot, **k):
    set_name = getattr(thing, 'setName', None)
    if not set_name:
        return
    sets = creature.equipmentSets
    sets[set_name] = sets.get(set_name, 0) + 1
    _update_set(creature, set_name)

def on_unequip(creature, thing, slot, **k):
    set_name = getattr(thing, 'setName', None)
    if not set_name:
        return
    sets = creature.equipmentSets
    count = sets.get(set_name, 0)
    if count <= 1:
        sets.pop(set_name, None)
    else:
        sets[set_name] = count - 1
    _update_set(creature, set_name)


# Register the callbacks for any item that defines a set name attribute
registerForAttr('equip', 'setName', on_equip)
registerForAttr('unequip', 'setName', on_unequip)


def _update_set(creature, set_name):
    bonuses = getattr(userconfig, 'equipmentSetBonuses', {}).get(set_name)
    if not bonuses:
        return
    count = creature.equipmentSets.get(set_name, 0)
    for pieces, stats in bonuses.items():
        cond_type = f"SETBONUS_{set_name}_{pieces}"
        if count >= pieces:
            if not creature.hasCondition(CONDITION_BUFF, cond_type):
                types = list(stats.keys())
                values = list(stats.values())
                if len(types) == 1:
                    boost = Boost(types[0], values[0], 10**9, subtype=cond_type)
                else:
                    boost = Boost(types, values, 10**9, subtype=cond_type)
                creature.condition(boost, CONDITION_REPLACE)
                creature.activeSetBonuses.add(cond_type)
        else:
            if cond_type in creature.activeSetBonuses:
                creature.loseCondition(CONDITION_BUFF, cond_type)
                creature.activeSetBonuses.remove(cond_type)
