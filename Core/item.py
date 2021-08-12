from dataclasses import dataclass


@dataclass
class Item:
    name: str
    description: str
    activate: str
    frequency: str
    effect: str
    item_level: int
    gp_cost: int
    # def __init__(self, name, description, activate, frequency, effect, item_level, gp_cost):
