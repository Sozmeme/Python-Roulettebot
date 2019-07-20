import unittest
from main import *
import random


class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.table = Table()
        self.player_depo = 1000
        self.player_winner = Player("player1", self.player_depo, self.table)
        self.player_loser = Player("player2", self.player_depo, self.table)
        self.bets = {
            "half": (2, [1, 2]),
            "parity": (2, ["odd", "even"]),
            "colour": (2, ["red", "black"]),
            "dozen": (4, [1, 2, 3]),
            "num": (72, [i for i in range(1, 37)])
        }

    def make_rand_bet(self):
        amount = random.randint(100, self.player_depo)
        bet_type = random.choice([i for i in self.bets.keys()])
        bet_val = random.choice(self.bets[bet_type][1])
        return amount, bet_type, bet_val

    def test_player_wins(self):
        pass

    def test_player_loses(self):
        pass



if __name__ == '__main__':
    unittest.main()
