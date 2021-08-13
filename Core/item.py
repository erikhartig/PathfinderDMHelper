from dataclasses import dataclass

from Core.link import PlayerItemLink


@dataclass
class Item:
    name: str
    description: str
    activate: str
    frequency: str
    effect: str
    item_level: int
    gp_cost: int
    _player: PlayerItemLink = None

    @property
    def player(self):
        if self._player:
            return self._player.player
        return None
