from test.framework import FrameworkTestGame, async_test
import config
import os
from game.item import Item

class TestPlayer(FrameworkTestGame):
    def test_class(self):
        self.assertIsInstance(self.player, Player)
        self.assertIsInstance(self.player, Creature)

    def test_talking(self):
        # These are NOT globals.
        from game.creature_talking import PlayerTalking, CreatureTalking
        
        self.assertIsInstance(self.player, PlayerTalking)
        self.assertIsInstance(self.player, CreatureTalking)
        self.player.say("Hello world!")
        
    def test_move(self):
        # These are NOT globals.
        from game.creature_movement import CreatureMovement

        self.assertIsInstance(self.player, CreatureMovement)
        newPosition = self.player.positionInDirection(SOUTH)

        self.player.move(SOUTH)
        
        self.assertEqual(newPosition, self.player.position)
        
    def test_teleport(self):
        newPosition = self.player.positionInDirection(SOUTH)
        self.player.teleport(newPosition)
        
        self.assertEqual(newPosition, self.player.position)
        
    def test_attackinheritence(self):
        """ A bug reported here: http://vapus.net/forum/pyot-opentibia-server-287/debug-serious-bugs-thread-2925-100/#post31523 """
        # This should NOT raise.
        self.player.cancelTarget(None)

    def test_losetarget(self):
        """ A test for this bug (#75): http://vapus.net/forum/project.php?issueid=75 """
        target = self.setupPlayer()

        self.assertTrue(target)

        self.player.target = target
        self.player.targetMode = 2

        pos = Position(1015, 1000, 7)
        self.player.teleport(pos, force=True)

        self.assertEqual(self.player.position, pos)
        self.assertEqual(self.player.target, None)
        self.assertEqual(self.player.targetMode, 0)

    def test_summon(self):
        """ A test for bug #87 """
        position = self.player.positionInDirection(NORTH)
        summon = self.player.summon("Wolf", position)

        self.assertTrue(summon)
        self.assertIn(summon, self.player.activeSummons)
        self.assertIn(summon, position.getTile().creatures())
        self.assertEqual(summon.master, self.player)

    def test_magic_level_formula_compatibility(self):
        orig = config.magicLevelFromManaFormula
        try:
            config.magicLevelFromManaFormula = lambda n: 1
            p1 = self.virtualPlayer(1001, "P1")
            self.assertEqual(p1.data["maglevel"], 1)
            self.destroyPlayer(p1)

            def two(n, c):
                return 2

            config.magicLevelFromManaFormula = two
            p2 = self.virtualPlayer(1002, "P2")
            self.assertEqual(p2.data["maglevel"], 2)
            self.destroyPlayer(p2)
        finally:
            config.magicLevelFromManaFormula = orig

    def test_level_up_restores_health_and_mana(self):
        level = self.player.data["level"]
        # reduce health and mana to non-full values
        self.player.data["health"] = 1
        self.player.data["mana"] = 1

        self.player.setLevel(level + 1)

        self.assertEqual(self.player.data["health"], self.player.data["healthmax"])
        self.assertEqual(self.player.data["mana"], self.player.data["manamax"])

    def test_item_serial_visibility(self):
        item = Item(100)
        item.rarity_description = "Rarity: Epic"
        item.rarity_serial = "SERIAL"

        self.player.data["group_id"] = 1
        text = item.description(self.player)
        self.assertIn("Rarity: Epic", text)
        self.assertNotIn("SERIAL", text)

        self.player.data["group_id"] = config.adminGroupId
        text = item.description(self.player)
        self.assertIn("SERIAL", text)

    def test_death_teleports_to_town(self):
        new_pos = Position(1010, 1000, 7)
        self.player.teleport(new_pos)
        self.player.modifyHealth(-1000)

        town_pos = Position(*game.map.mapInfo.towns[self.player.data['town_id']][1])
        self.assertTrue(self.player.alive)
        self.assertEqual(self.player.position, town_pos)

    def test_stuck_command(self):
        self.player.teleport(Position(1015, 1000, 7))
        town_pos = Position(*game.map.mapInfo.towns[self.player.data['town_id']][1])
        game.scriptsystem.get("talkaction").run("!stuck", creature=self.player, text="")
        self.assertEqual(self.player.position, town_pos)

    def test_report_command_creates_file_and_rewards(self):
        files_before = set(os.listdir('logs'))
        msg = 'This is a bug'
        game.scriptsystem.get("talkactionFirstWord").run("!report", creature=self.player, text=msg)

        files_after = set(os.listdir('logs'))
        new_files = list(files_after - files_before)
        self.assertEqual(len(new_files), 1)
        fname = new_files[0]
        self.assertTrue(fname.startswith(f"Error.{self.player.name()}"))
        with open(os.path.join('logs', fname)) as fh:
            self.assertEqual(fh.read(), msg)

        reward_id = getattr(config, 'reportRewardItemId', 2160)
        count = self.player.itemCount(Item(reward_id))
        self.assertEqual(count, 1)
