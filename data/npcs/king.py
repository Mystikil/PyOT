import sql
king = game.npc.genNPC("The King", (332, 20, 39, 45, 7, 0, 0))
king.setWalkable(False)
accept = ('Yes', 'Ok', 'Sure')
king.greet("Greetings %(playerName)s. I can {promote} you.")
 
class Promotion(game.npc.ClassAction):
    def action(self):
        self.on.onSaid('promote', self.promotion)

    def promotion(self, npc, player):
        npc.sayTo(player, "Professions are no longer available.")
 
king.module(Promotion)
