# Player
# Table
# Bet
from random import randrange, choice


class Player:

    def __init__(self, name, depo, table):
        """
        Player object
        :param name:
        :param depo:
        :param table:
        """
        self.name = name
        self.depo = depo
        self.table = table

    def make_bet(self, amount, cond: tuple):
        """
        Create bet with win condition, add it on table
        """

        Player.check_valid(self, cond)

        if 0 < amount < self.depo:
            self.depo -= amount
            self.table.bet_list.append(Bet(amount, cond, self))
        elif amount > self.depo:
            print(choice(["You can't bet more than you have", "Out of money", "Cannot afford", "Need more money"]))
        elif amount < 0:
            print(choice(["You can't bet less than 1!", "Nice try", "Try one more time"]))

    def check_valid(self, cond: tuple):
        # TODO: Make different messages
        print(f"Attempt to bet {cond}")
        if len(cond) != 2:
            raise BetError('Wrong value(s)')
        elif cond[0] not in ['num', 'colour', 'half', 'dozen', 'parity']:
            raise BetError('Wrong value(s)')
        elif cond[0] == 'num' and (cond[1] > 36 or cond[1] < 1):
            raise BetError('Wrong value(s)')
        elif cond[0] == 'colour' and cond[1] not in ['black', 'red']:
            raise BetError('Wrong value(s)')
        elif cond[0] == 'half' and cond[1] not in [1, 2]:
            raise BetError('Wrong value(s)')
        elif cond[0] == 'dozen' and cond[1] not in [1, 2, 3]:
            raise BetError('Wrong value(s)')
        elif cond[0] == 'parity' and cond[1] not in ['odd', 'even']:
            raise BetError('Wrong value(s)')


class Bet:
    coefs = {'num': 72, 'colour': 2, 'half': 2, 'dozen': 4, 'parity': 2}

    def __init__(self, amount, condition: tuple, player: Player):
        """
        Bet made by player.
        """
        self.amount = amount
        self.condition = condition
        self.player = player

    def check_for_win(self, result):
        """
        Returns True if bet wins
        """
        return self.condition in result.items()

    @property
    def coef(self):
        """
        Determine self.coef based on self.condition
        """
        return Bet.coefs[self.condition[0]]


class Table:
    """
    Has bet list, random generator
    """
    desk = {
        "red": [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
        "black": [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    }

    def __init__(self):
        self.bet_list = []
        self.result = None
        self.winners = []

    def ball_throw(self):
        """
        Result contains colour, num, half and dozen in which num is -> (num, colour, half, dozen)
        """
        num = randrange(1, 37)
        parity = ["odd", "even"][num % 2 == 0]
        colour = ["red", "black"][num in Table.desk["black"]]  # исправлено
        half = [1, 2][19 <= num <= 36]
        if 0 <= num <= 12:
            dozen = 1
        elif 13 <= num <= 24:
            dozen = 2
        else:
            dozen = 3

        self.result = {'num': num, 'colour': colour, 'half': half, 'dozen': dozen, 'parity': parity}

    def update_depo(self):
        """
        Update depo for each win bet owner according to bet coef
        """
        while self.bet_list:
            bet = self.bet_list.pop()
            if bet.check_for_win(self.result):
                self.winners.append(bet.player.name)
                bet.player.depo += bet.amount * bet.coef


    def no_more_bets(self):
        print('Ball has been thrown!')
        self.ball_throw()
        print('Current result: {}'.format(self.result))
        self.update_depo()
        print('Lucky ones: {}'.format(self.winners))
        self.winners.clear()


class BetError(Exception):
    """
    BetError class
    """




###################################################
# Пример работы
# table = Table()
# player1 = Player("Player 1", 1000, table)
# player2 = Player("Player 2", 1000, table)
# player1.make_bet(100, {"half": 1})
# player2.make_bet(200, {"color": "red"})
# table.no_more_bets()