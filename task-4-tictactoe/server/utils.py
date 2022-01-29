import argparse
import socket
from string import ascii_uppercase as upper


class TicTacToe:
    def __init__(self, size: int):
        if size < 3 or size > 26:
            raise Exception("Gaming grid size must be 3-26.")
        self.size = size
        self.grid = [[" "] * size for i in range(size)]
        self.players = {1: "X", 2: "O"}
        self.error = {
            0: f"\nWrong input format, must be 1 uppercase letter (from A to {chr(64+size)}) and a number (from 1 to {size}).\n",
            1: "\nCell is used\n",
        }

    def turn(self, player: int, x: str, y: str):
        x, y = ord(x) - 65, int(y) - 1
        self.grid[x][y] = self.players[player]
        return self.win(player, x, y)

    def win(self, player: int, x: int, y: int):
        l = self.size
        # Checking diagonal line from upper left to lower right corner
        if x == y and all(self.grid[i][i] == self.players[player] for i in range(l)):
            return True
        # checking diagonal line from lower left to upper right corner
        if x == l - 1 - y and all(
            self.grid[l - 1 - i][i] == self.players[player] for i in range(l)
        ):
            return True
        # chechking vertical and horizontal lines
        for i in range(l):
            if all(self.grid[i][j] == self.players[player] for j in range(l)) or all(
                self.grid[j][i] == self.players[player] for j in range(l)
            ):
                return True
        return False

    def tie(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == " ":
                    return False
        return True

    def valid(self, data: str):
        if len(data) != 2:
            return False, 0
        x, y = data
        if (
            x not in upper
            or ord(x) - 65 < 0
            or ord(x) - 65 > self.size
            or not y.isdigit()
            or int(y) - 1 < 0
            or int(y) - 1 > self.size
        ):
            return False, 0
        if self.grid[ord(x) - 65][int(y) - 1] != " ":
            return False, 1
        return True, None

    def status(self):
        s = self.size
        l = len(str(s))
        a = (
            "|\n  " + "---".join(["|" for i in range(s + 1)]) + "\n"
        )  # It will look like this:  |---|---|---|
        status = (
            "\n  |"
            + "|".join(
                [(len(str(i + 1)) % 2) * " " + str(i + 1) + " " for i in range(s)]
            )
            + a
        )
        # It will look like this:  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |10 |11 |
        for i in range(s):
            status += (
                f" {chr(65+i)}|" + "|".join([f" {j} " for j in self.grid[i]]) + a
            )  # It will look like this:   A|   |   |   |
        return status
        """
        As a result of this method's work, you can get following:
          | 1 | 2 | 3 |
          |---|---|---|
         A|   |   |   |
          |---|---|---|
         B|   |   |   |
          |---|---|---|
         C|   |   |   |
          |---|---|---|
        """


def create_parser():  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("address", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("size", type=int)
    return parser


def turn_first_player(game: TicTacToe):
    print("\nMake your turn\n")
    while True:
        data = input().split()
        res = game.valid(data)
        if res[0]:
            x, y = data
            break
        print(game.error[res[1]])
    return game.turn(1, x, y)


def turn_second_player(game: TicTacToe, conn):  # pragma: no cover
    conn.send("\nMake your turn\n".encode())
    while True:
        data = conn.recv(8192).decode("utf-8").split()
        res = game.valid(data)
        if res[0]:
            x, y = data
            break
        conn.send(game.error[res[1]].encode())
    return game.turn(2, x, y)


def update_all(message, conn):  # pragma: no cover
    print(message)
    conn.send(message.encode())


def start_server(host: str, port: int, size: int):  # pragma: no cover
    m = f"""\nWelcome to tic-tac-toe!
This is the game, where you can unleash your whole fantasy... to combinate "X" and "O".
First player getting {size} cells in a row, column or diagonal wins.
"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    game = TicTacToe(size)
    print("\nWaiting for 2nd player\n")
    conn, addr = s.accept()
    update_all(m, conn)
    while True:
        update_all(game.status(), conn)
        conn.send("\n1st player makes turn\n".encode())
        if turn_first_player(game):
            update_all(game.status() + f"\nPlayer 1 wins!\n", conn)
            break
        if game.tie():
            update_all(game.status() + "It's tie!", conn)
            break
        conn.send("\nPlayer 1 made turn\n".encode())
        update_all(game.status(), conn)
        print("\n2nd player makes turn\n")
        if turn_second_player(game, conn):
            update_all(game.status() + f"\nPlayer 2 wins!\n", conn)
            break
        if game.tie():
            update_all(game.status() + "It's tie!", conn)
            break
        print("\nPlayer 2 made turn\n")
    conn.close()
