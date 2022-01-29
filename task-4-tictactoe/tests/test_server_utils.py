from builtins import input

import pytest

import server.utils as s


def test_win_vertical():
    game = s.TicTacToe(3)
    game.turn(1, "A", "1")
    game.turn(1, "A", "2")
    assert game.turn(1, "A", "3")


def test_win_horizontal():
    game = s.TicTacToe(3)
    game.turn(1, "A", "1")
    game.turn(1, "B", "1")
    assert game.turn(1, "C", "1")


def test_win_diagonal():
    game = s.TicTacToe(3)
    game.turn(1, "A", "1")
    game.turn(1, "B", "2")
    assert game.turn(1, "C", "3")


def test_win_diagonal_2():
    game = s.TicTacToe(3)
    game.turn(1, "A", "3")
    game.turn(1, "B", "2")
    assert game.turn(1, "C", "1")


def test_tie():
    game = s.TicTacToe(3)
    game.turn(1, "B", "1")
    game.turn(2, "A", "1")
    game.turn(1, "B", "2")
    game.turn(2, "B", "3")
    assert not game.tie()
    game.turn(1, "C", "2")
    game.turn(2, "A", "2")
    game.turn(1, "A", "3")
    game.turn(2, "C", "3")
    game.turn(1, "C", "1")
    assert game.tie()


def test_less_grid():
    with pytest.raises(Exception):
        game = TicTacToe(2)


def test_greater_grid():
    with pytest.raises(Exception):
        game = TicTacToe(30)


def test_valid():
    game = s.TicTacToe(5)
    assert game.valid(["A", "1"])[0]
    game.turn(1, "A", "1")
    assert not game.valid(["A", "1"])[0]
    assert not game.valid(["Wrong", "input", "format"])[0]
    assert not game.valid(["A", "74"])[0]


def test_status():
    game = s.TicTacToe(3)
    assert (
        game.status()
        == """
  | 1 | 2 | 3 |
  |---|---|---|
 A|   |   |   |
  |---|---|---|
 B|   |   |   |
  |---|---|---|
 C|   |   |   |
  |---|---|---|
"""
    )


def test_turn_1(monkeypatch):
    def func():
        for i in ["B 1", "B 2", "B 3"]:
            yield i

    a = func()
    monkeypatch.setattr("builtins.input", lambda: next(a))
    game = s.TicTacToe(3)
    s.turn_first_player(game)
    s.turn_first_player(game)
    assert s.turn_first_player(game)
