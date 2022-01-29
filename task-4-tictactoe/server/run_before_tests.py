import builtins

from utils import start_server

if __name__ == "__main__":

    def func():
        for i in ["A 1", "A 2", "C 1"]:
            yield i

    a = func()
    builtins.input = lambda: next(a)
    start_server("localhost", 5000, 3)
