from typing import Dict, NamedTuple
from uuid import uuid4


class Client(NamedTuple):
    id: str
    photo: str
    name: str
    phone_num: str
    e_mail: str


clients: Dict[str, Client] = {}


def add_client(name, num, mail) -> Client:
    client = Client(
        id=uuid4().hex, name=name, phone_num=num, e_mail=mail, photo="no_photo.jpg"
    )
    clients[client.id] = client
    return client


def change_path(id, postfix) -> None:
    clients[id] = clients[id]._replace(photo=postfix)


def remove_client(client_id: str) -> None:
    clients.pop(client_id)


def clear_clients():
    clients = {}
