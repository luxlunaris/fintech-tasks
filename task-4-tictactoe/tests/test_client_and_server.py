from builtins import input

import client.utils as c


def test_client(monkeypatch, capsys):
    def func():
        for i in ["B 1", "B 2", "B 3"]:
            yield i

    a = func()
    monkeypatch.setattr("builtins.input", lambda: next(a))
    c.connect("localhost", 5000)
    captured = capsys.readouterr()
    assert "Player 2 wins" in captured.out
