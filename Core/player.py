from dataclasses import dataclass
from math import floor

from Core.roll_dice import roll_d20


class AbilityScore:
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value

    def roll(self):
        result = roll_d20() + self.get_modifier()
        if result >= 0:
            return result
        return 0

    def set(self, value):
        self.value = value

    def get_modifier(self):
        return floor((self.value - 10) / 2)


@dataclass
class AbilityScores:
    strength: AbilityScore
    dexterity: AbilityScore
    constitution: AbilityScore
    intelligence: AbilityScore
    wisdom: AbilityScore
    charisma: AbilityScore


@dataclass
class Player:
    ability_scores: AbilityScores
