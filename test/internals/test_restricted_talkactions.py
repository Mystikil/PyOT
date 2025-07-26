from test.framework import FrameworkTestGame
import game.functions

class TestRestrictedTalkactions(FrameworkTestGame):
    def test_player_group_flag_allows_execution(self):
        game.functions.groups[2] = ("Special", ["INVISIBLE"])
        self.player.data["group_id"] = 2
        self.player.data["account_group_id"] = 1
        before = len(self.client._packets)
        game.scriptsystem.get("talkaction").run("/invisible", creature=self.player, text="")
        self.assertTrue(self.player.hasCondition(CONDITION_INVISIBLE))
        self.assertGreater(len(self.client._packets), before)

    def test_player_without_flags_is_denied(self):
        game.functions.groups[1] = ("Player", [])
        game.functions.groups[2] = ("Account", [])
        self.player.data["group_id"] = 1
        self.player.data["account_group_id"] = 2
        before = len(self.client._packets)
        game.scriptsystem.get("talkaction").run("/invisible", creature=self.player, text="")
        self.assertFalse(self.player.hasCondition(CONDITION_INVISIBLE))
        self.assertEqual(len(self.client._packets), before)

