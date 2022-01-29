import argparse
import socket


def create_parser():  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("address", type=str)
    parser.add_argument("port", type=int)
    return parser


def connect(adress, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((adress, port))
    print(s.recv(8192).decode("utf-8"))
    while True:
        data = s.recv(8192).decode("utf-8")
        print(data)
        if any(
            k in data for k in ["Make your turn", "Wrong input format", "Cell is used"]
        ):
            s.sendall(input().encode())
        if any(k in data for k in ["tie", "win"]):
            break
    s.close()
