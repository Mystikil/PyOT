from test.framework import FrameworkTestGame
import game.functions

class TestAccountGroupAccess(FrameworkTestGame):
    def test_account_group_grants_access(self):
        game.functions.groups[1] = ("Player", [])
        game.functions.groups[4] = ("Gamemaster", ["TELEPORT"])
        self.player.data["group_id"] = 1
        self.player.data["account_group_id"] = 4
        new_pos = Position(1000, 1001, 7)
        game.scriptsystem.get("talkactionFirstWord").run("/goto", creature=self.player, text="1000,1001,7")
        self.assertEqual(self.player.position, new_pos)

    def test_no_account_group_no_access(self):
        game.functions.groups[1] = ("Player", [])
        self.player.data["group_id"] = 1
        self.player.data["account_group_id"] = 1
        old_pos = self.player.position.copy()
        game.scriptsystem.get("talkactionFirstWord").run("/goto", creature=self.player, text="1000,1001,7")
        self.assertEqual(self.player.position, old_pos)
