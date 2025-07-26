from data.scripts.skills import SKILL_NAMES, SKILL_COLORS
from game.const import SKILL_FIRST, SKILL_LAST
# The script system automatically exposes a global ``register`` function via
# ``builtins`` during loading. Importing it from ``data.scripts`` leads to an
# ImportError because ``data.scripts.__init__`` does not export ``register``.
# Using the builtin directly avoids the issue when this script is loaded.

@register('talkaction', '!skills')
def show_skills(creature, **k):
    lines = []
    for skill in range(SKILL_FIRST, SKILL_LAST + 1):
        name = SKILL_NAMES.get(skill, f'Skill {skill}')
        level = creature.skills.get(skill, 0)
        tries = creature.data['skill_tries'].get(skill, 0)
        goal = creature.skillGoals.get(skill, 1)
        pct = int((tries / goal) * 100) if goal else 0
        bar_len = 20
        filled = pct * bar_len // 100
        bar = '[' + '#' * filled + '-' * (bar_len - filled) + ']'
        lines.append(f"{name}: {level} {bar} {pct}%")
    text = '\n'.join(lines)
    if creature.client.version >= 960:
        dlg = creature.dialog('Skills', text, ['Ok'])
        creature.setWindowHandler(dlg, lambda x: None)
    else:
        creature.windowMessage(text)
    return False

