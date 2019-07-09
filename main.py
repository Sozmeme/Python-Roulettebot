# Player
# Table
# Bet
from random import randrange, choice


class Player:
    """
    Что нам надо знать про игрока?
    Имя, депо, стол
    Игрок может делать ставки на стол за которым сидит
    """

    def __init__(self, name, depo, table):
        self.name = name
        self.depo = depo
        self.table = table

    def make_bet(self, amount, cond: dict):
        """
        Create bet with win condition, add it on table
        """
        if self.depo >= amount:
            self.depo -= amount
        else:
            print(choice(["You can't bet more than you have", "Out of money", "Cannot afford", "Need more money"]))
        self.table.bet_list.append(Bet(amount, cond, self))


class Bet:
    coefs = {'num': 36, 'colour': 1, 'half': 1, 'dozen': 2}

    def __init__(self, amount, condition: dict, player: Player):  # TODO: добавить проверку длины словаря!
        """
        Bet made by player.
        """
        self.amount = amount
        # смотри строку 88, можешь использовать .update()
        # добавить коэффициенты
        self.condition = condition  # варианты: {"num": num}, {"colour": colour}, {"half": half}, {"dozen": half}
        self.player = player

    def check_for_win(self, result):
        """
        Returns True if bet wins
        """
        return self.condition.popitem() in result.items()

    @property
    def coef(self):
        """
        Determine self.coef based on self.condition
        """
        for key in self.condition:
            return Bet.coefs[key]


# Bet(100, {"half": 1}, Player()).coef


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

    def ball_throw(self):
        """
        Result contains colour, num, half and dozen in which num is -> (num, colour, half, dozen)
        """
        num = randrange(1, 37)
        colour = ["red", "black"][num in Table.desk["black"]]  # исправлено
        half = [1, 2][19 <= num <= 36]
        if 0 <= num <= 12:
            dozen = 1
        elif 13 <= num <= 24:
            dozen = 2
        else:
            dozen = 3

        self.result = {'num': num, 'colour': colour, 'half': half, 'dozen': dozen}  # TODO: добавить чет/нечет

    def update_depo(self):  # DONE?
        """
        Update depo for each win bet owner according to bet coef
        """
        while self.bet_list:
            bet = self.bet_list.pop()
            if bet.check_for_win(self.result):
                bet.player.depo += bet.amount * bet.coef

###################################################
# Пример работы
# table = Table()
# player1 = Player("Player 1", 1000, table)
# player2 = Player("Player 2", 1000, table)
# player1.make_bet(100, {"half": 1})
# player2.make_bet(200, {"color": "red"})
# table.ball_throw()
# table.update_depo()