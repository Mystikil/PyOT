from test.framework import FrameworkTestGame
import game.functions

class TestInvisibleCommand(FrameworkTestGame):
    def test_invisible_applies_condition_and_broadcasts(self):
        game.functions.groups[1] = ("Player", ["INVISIBLE"])
        self.player.data["group_id"] = 1
        self.player.data["account_group_id"] = 1
        before = len(self.client._packets)
        game.scriptsystem.get("talkaction").run("/invisible", creature=self.player, text="")
        self.assertTrue(self.player.hasCondition(CONDITION_INVISIBLE))
        self.assertGreater(len(self.client._packets), before)
