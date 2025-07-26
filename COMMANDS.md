# Game Commands

This document lists the built in player commands available in PyOT.
Commands are registered via the talkaction script system. Some commands
may require special access rights (see [Permissions](README.md#permissions)).

## Administrative commands

- `/ban <player> <length> <reason>` – ban a player.
- `/ipban <ip|player> <length> <reason>` – ban an IP address.
- `/accban <account> <length> <reason>` – ban an account.
- `/ba <message>[;color]` – broadcast a message anonymously.
- `/b <message>[;color]` – broadcast a message with your name.
- `/i <item name or id>[, count]` – create items by name or id.
- `/in <item name>, [count]` – alias for `/i`.
- `saveme` – save your character.
- `saveall` – save all characters.

## Teleportation

- `teleport <x>,<y>,<z>` – teleport yourself.
- `fteleport <x>,<y>,<z>` – force teleport ignoring protection.
- `/t` – teleport to your temple or teleport another player there.
- `/goto <name>` – teleport to a player or coordinates.
- `/a <tiles>[,force]` – teleport several tiles forward.
- `/up` / `/down` – move one floor up or down.

## House management

- `aleta sio` – edit guest list of the current house.
- `aleta grav` – edit door access list.
- `aleta som` – edit sub‑owners.
- `alana sio <player>` – kick a player from your house.

## Miscellaneous

- `set` – spawn an item at a position.
- `t` – spawn the last item again.
- `mypos` – print your current position.
- `speed <value>` – set your speed.
- `reload` – reload all scripts.
- `pop` – test container functions (developer).
- `exp <amount>` – modify your experience.
- `s <monster>` – spawn a monster.
- `n <npc>` – spawn an NPC.
- `res <monster>` – summon a monster if you have enough mana.
- `setowner <house id>` – set yourself as house owner.
- `poisonme` – apply poison condition.
- `conditionme` – apply several conditions.
- `conditionpercent` – apply percentage based conditions.
- `restore` – restore health and mana.
- `info <position>` – list creatures and items on a tile.
- `boostme` – temporary stat boost.
- `aime` – start a simple AI example.
- `market` – open the market window.
- `forward!` – walk one step forward.
- `die` – lose a lot of health.
- `immune` – make yourself unattackable.
- `/invisible` – become invisible for a short time.
- `kill me now` – instantly die.
- `8.6 dialog` – open a test dialog.
- `freeze!` – delay your movement for a short time.
- `newinventory` – give yourself a basic inventory.
- `pm` – play a test sound.
- `/pos` – manage saved teleport locations.
- `/lang` or `/language` – change client language.
- `/war <accept|reject|cancel> <guild>` – manage war invitations.
- `/war invite <guild> <stakes> <duration> <frags>` – invite a guild to war.
- `/balance <pick|donate> <amount>` – manage guild bank balance.
- `/balance` – show guild bank balance.
- `begin quest` – start a quest from the example scripts.
- `hello world` – finish the example quest.
- `missions quest` – start the mission quest example.

The list above contains the commands distributed with PyOT. Additional
scripts may register further talkactions.
