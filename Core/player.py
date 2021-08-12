from dataclasses import dataclass
from math import floor

from Core.roll_dice import roll_d20


class Score:
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value

    def roll(self):
        """
        Placeholder function for roll
        """

    def set(self, value):
        self.value = value


class AbilityScore(Score):
    def roll(self):
        result = roll_d20() + self.get_modifier()
        if result >= 0:
            return result
        return 0

    def get_modifier(self):
        return floor((self.value - 10) / 2)


class SkillScore(Score):
    def roll(self):
        result = roll_d20() + self.value
        if result >= 0:
            return result
        return 0


@dataclass
class AbilityScores:
    strength: AbilityScore
    dexterity: AbilityScore
    constitution: AbilityScore
    intelligence: AbilityScore
    wisdom: AbilityScore
    charisma: AbilityScore


@dataclass
class Skills:
    acrobatics: SkillScore
    arcana: SkillScore
    athletics: SkillScore
    crafting: SkillScore
    deception: SkillScore
    diplomacy: SkillScore
    intimidation: SkillScore
    lore: SkillScore
    medicine: SkillScore
    nature: SkillScore
    occultism: SkillScore
    performance: SkillScore
    religion: SkillScore
    society: SkillScore
    stealth: SkillScore
    survival: SkillScore
    thievery: SkillScore


@dataclass
class Player:
    name: str
    ability_scores: AbilityScores
    skills: Skills
