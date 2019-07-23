from main import *
import json


# TODO создать базу данных игроков json, спросить число игроков, создать игроков, до команды "stop" крутить раунды

class GameManager:

    def __init__(self, default_depo=1000):
        self.table = Table()
        self.name_list = []
        self.player_list = []
        self.default_depo = default_depo
        self.greeting = """
                        Hello! It's my very first game and here you can play roulette!\n
                        You can bet on colour(black/red), number(1-36), parity(odd/even), half(1/2) and dozen(1-3).\n
                        To exit press CTRL + C.\n
                        """
        with open('player_data.json') as f:
            self.player_data = json.load(f)

    def set_up(self):
        """
        Создание игроков и их "усаживание" за стол
        """
        count = int(input("Input the number of new players\n"))

        for i in range(count): # TODO дать игроку возможность получить депо из прошлой игры
            name = input('Player {}, enter your name\n'.format(i + 1))
            self.player_list.append(Player(name, self.default_depo, self.table))

    def play_round(self):
        """
        Single game round
        :return:
        """
        for player in self.player_list:
            while True:
                try:
                    player.make_bet(*self.handle_player_input(player))
                    break
                except (BetError, ValueError) as e:
                    print(e)

        print('Now all bets are made!')
        self.table.no_more_bets()

    def handle_player_input(self, player):
        raw_input = input("{}, your turn to make a bet!\n".format(player.name)).strip().split()
        # print(raw_input)
        if len(raw_input) != 3:
            raise ValueError("Error! Enter bet amount, type and value separated with space.")
        amount, bet_type, bet_val = raw_input

        if bet_val.isdigit():
            bet_val = int(bet_val)
        return int(amount), (bet_type, bet_val)

    def start_game(self):
        """
        Initialize game beginning
        :return:
        """
        print("Prepare your money!")
        self.cur_depo()
        while True:
            self.play_round()
            print("Current deposits:")
            self.cur_depo()

    def stop_game(self):
        print("Good bye! It was very nice to get your money!")
        exit()

    def cur_depo(self):
        for player in self.player_list:
            print('{} - {}'.format(player.name, player.depo))


if __name__ == '__main__':
    manager = GameManager()
    print(manager.greeting)
    manager.set_up()
    try:
        manager.start_game()
    except KeyboardInterrupt:
        manager.stop_game()
