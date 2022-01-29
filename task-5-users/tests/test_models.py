from server.models import (
    Client,
    add_client,
    change_path,
    clients,
    remove_client,
)


def test_clients():
    c1 = add_client("name", "num", "mail")
    c2 = add_client("name1", "num1", "mail1")
    assert len(clients) == 2
    remove_client(c1.id)
    assert len(clients) == 1


def test_path():
    add_client("name", "num", "mail")
    add_client("name1", "num1", "mail1")
    for id in clients:
        change_path(id, str(id) + ".jpg")
        assert clients[id].photo == str(id) + ".jpg"
