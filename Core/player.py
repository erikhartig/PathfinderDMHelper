from dataclasses import dataclass, field
from math import floor

from Core.link import PlayerItemLink
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
    _items: [PlayerItemLink] = field(default_factory=list)

    def assign_item(self, item):
        link = PlayerItemLink(self, item)
        self._items.append(link)
        item._player = link

    def remove_item(self, item):
        for item_links in self._items:
            if item_links.item == item:
                item_links.item._player = None
                self._items.remove(item_links)
                return

    @property
    def items(self):
        items = []
        for item_links in self._items:
            items.append(item_links.item)
        return items
