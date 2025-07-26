from test.framework import FrameworkTestGame

class TestMonster(FrameworkTestGame):
    def test_corpses(self):
        # For "special" monsters with no corpse or so.
        ignore = ("Northern Pike", "Rift Worm", "Insect Swarm", "Fish", "Slime", "Butterfly", "Son Of Verminor")

        printer = self.fail
        #printer = sys.__stdout__.write
        for monsterName in game.monster.monsters:
            if monsterName in ignore:
                continue

            monster = getMonster(monsterName)
            if not monster.data['corpse']:
                printer("[ERROR] Monster %s got no corpse!\n" % monsterName)
                continue
            corpse = monster.data['corpse']
            item = Item(corpse)
            if not item.name:
                printer("[WARNING] Monster %s (corpse: %d) doesn't have a name, likely invalid\n" % (monsterName, corpse))

            else:
                name = item.name.lower()
                if not "dead" in name and not "slain" in name and not "undead" in name and not "remains" in name and not "lifeless" in name:
                    printer("[WARNING] Monster %s (corpse: %d) doesn't have dead/slain/undead/remains/lifeless in it's name, likely invalid\n" % (monsterName, corpse))
                    continue

            if not item.corpseType:
                printer("[WARNING] Monster %s corpse (%d) don't have a corpseType\n" % (monsterName, corpse))

    def test_ignores_flagged_players(self):
        """Monsters should ignore players with the IGNORED_BY_CREATURES flag."""
        # Ensure the player has the flag via group assignment
        self.player.data["group_id"] = 3  # group 3 contains IGNORED_BY_CREATURES
        self.player.data["account_group_id"] = 3

        wolf = getMonster("Wolf").spawn(self.player.positionInDirection(NORTH), spawnDelay=0, radius=0)
        try:
            wolf.targetCheck([self.player])
            self.assertIsNone(wolf.target)
        finally:
            wolf.turnOffBrain()
            wolf.despawn()
