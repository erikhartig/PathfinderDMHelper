import pickle
from dataclasses import dataclass, field

from Core.item import Item
from Core.player import Player
from paths import ITEMS, PLAYERS


def save_items(items):
    save_file(ITEMS, items)


def load_items():
    return load_file(ITEMS)


def save_players(players):
    save_file(PLAYERS, players)


def load_players():
    return load_file(PLAYERS)


def load_file(path):
    if not path.exists():
        return []
    with open(path, 'rb') as item_file:
        items = pickle.load(item_file)
    return items


def save_file(path, items):
    with open(path, 'wb') as item_file:
        pickle.dump(items, item_file, pickle.HIGHEST_PROTOCOL)


@dataclass
class DataStore:
    players: [Player] = field(default_factory=list)
    items: [Item] = field(default_factory=list)
