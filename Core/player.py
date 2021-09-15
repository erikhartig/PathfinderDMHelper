from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from math import floor
from typing import List

from sqlalchemy import Column, orm, create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.pool import StaticPool

from Core.roll_dice import roll_d20

mapper_registry = registry()
Session = None
engine = None


def set_engine(engine_to_use):
    global Session
    global engine
    if Session:
        Session.close_all()
    if engine:
        engine.dispose()
    engine = engine_to_use
    mapper_registry.metadata.create_all(engine)
    Session = sessionmaker(engine, expire_on_commit=False)


def get_session():
    """
    Returns:
        sessionmaker: an object used to construct new sessions
    """
    return Session


class Score(int):
    def __init__(self, value):
        super().__init__()
        self.value = value

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


@mapper_registry.mapped
@dataclass
class Player:
    __table__ = Table(
        "player",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column("acrobatics", Integer),
        Column("arcana", Integer),
        Column("athletics", Integer),
        Column("crafting", Integer),
        Column("deception", Integer),
        Column("diplomacy", Integer),
        Column("intimidation", Integer),
        Column("lore", Integer),
        Column("medicine", Integer),
        Column("nature", Integer),
        Column("occultism", Integer),
        Column("performance", Integer),
        Column("religion", Integer),
        Column("society", Integer),
        Column("stealth", Integer),
        Column("survival", Integer),
        Column("thievery", Integer),
        Column("strength", Integer),
        Column("dexterity", Integer),
        Column("constitution", Integer),
        Column("intelligence", Integer),
        Column("wisdom", Integer),
        Column("charisma", Integer),
    )
    id: int = field(init=False)
    name: str = ""
    acrobatics: SkillScore or int = SkillScore(0)
    arcana: SkillScore or int = SkillScore(0)
    athletics: SkillScore or int = SkillScore(0)
    crafting: SkillScore or int = SkillScore(0)
    deception: SkillScore or int = SkillScore(0)
    diplomacy: SkillScore or int = SkillScore(0)
    intimidation: SkillScore or int = SkillScore(0)
    lore: SkillScore or int = SkillScore(0)
    medicine: SkillScore or int = SkillScore(0)
    nature: SkillScore or int = SkillScore(0)
    occultism: SkillScore or int = SkillScore(0)
    performance: SkillScore or int = SkillScore(0)
    religion: SkillScore or int = SkillScore(0)
    society: SkillScore or int = SkillScore(0)
    stealth: SkillScore or int = SkillScore(0)
    survival: SkillScore or int = SkillScore(0)
    thievery: SkillScore or int = SkillScore(0)
    strength: AbilityScore or int = AbilityScore(10)
    dexterity: AbilityScore or int = AbilityScore(10)
    constitution: AbilityScore or int = AbilityScore(10)
    intelligence: AbilityScore or int = AbilityScore(10)
    wisdom: AbilityScore or int = AbilityScore(10)
    charisma: AbilityScore or int = AbilityScore(10)
    items: List[Item] = field(default_factory=list)

    __mapper_args__ = {  # type: ignore
        "properties": {
            "items": relationship("Item", back_populates="player")
        }
    }

    @orm.reconstructor
    def init_on_load(self):
        self._convert_scores()

    def __post_init__(self):
        self._convert_scores()
        with get_session().begin() as db:
            db.add(self)

    def save(self):
        get_session().close_all()
        with get_session().begin() as db:
            db.add(self)

    def delete(self):
        get_session().close_all()
        with get_session().begin() as db:
            db.delete(self)

    def _convert_scores(self):
        annos = self.__annotations__
        for score_name, score_value in vars(self).items():
            if score_name in annos and "SkillScore" in annos[score_name] and not isinstance(score_value, Score):
                self.__setattr__(score_name, SkillScore(score_value))
            if score_name in annos and "AbilityScore" in annos[score_name] and not isinstance(score_value, Score):
                self.__setattr__(score_name, AbilityScore(score_value))

    def add_item(self, item):
        get_session().close_all()
        with get_session().begin() as db:
            db.add(self)
            self.items.append(item)

    def remove_item(self, item):
        get_session().close_all()
        with get_session().begin() as db:
            db.add(self)
            self.items.remove(item)

    def get_ability_scores(self):
        ability_scores = {}
        for ability in get_ability_fields():
            ability_scores[ability] = self.__getattribute__(ability)
        return ability_scores

    def get_skill_scores(self):
        skill_scores = {}
        for skill in get_skill_fields():
            skill_scores[skill] = self.__getattribute__(skill)
        return skill_scores


@mapper_registry.mapped
@dataclass
class Item:
    __table__ = Table(
        "item",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("player_id", Integer, ForeignKey("player.id", onupdate="cascade")),
        Column("name", String()),
        Column("description", String()),
        Column("item_level", Integer),
        Column("gp_cost", Integer),
        Column("frequency", String()),
        Column("effect", String()),
        Column("activate", String()),
    )
    name: str
    description: str
    item_level: int
    gp_cost: int
    activate: str = ""
    frequency: str = ""
    effect: str = ""
    id: int = field(init=False)
    player_id: int = field(init=False)
    player: Player = None

    __mapper_args__ = {  # type: ignore
        "properties": {
            "player": relationship("Player", back_populates="items")
        }
    }

    def __post_init__(self):
        with get_session().begin() as db:
            db.add(self)

    def delete(self):
        get_session().close_all()
        with get_session().begin() as db:
            db.delete(self)

    def save(self):
        get_session().close_all()
        with get_session().begin() as db:
            db.add(self)

    def get_fields(self):
        return {
            "name": self.name,
            "description": self.description,
            "item_level": self.item_level,
            "gp_cost": self.gp_cost,
            "activate": self.activate,
            "frequency": self.frequency,
            "effect": self.effect
        }


def get_all_players(db=None):
    if db:
        players = db.query(Player)
    else:
        with get_session().begin() as db:
            players = db.query(Player)
    return players.all()


def get_all_items():
    with get_session().begin() as db:
        items = db.query(Item)
    return items.all()


def get_skill_fields():
    return ["acrobatics",
            "arcana",
            "athletics",
            "crafting",
            "deception",
            "diplomacy",
            "intimidation",
            "lore",
            "medicine",
            "nature",
            "occultism",
            "performance",
            "religion",
            "society",
            "stealth",
            "survival",
            "thievery", ]


def get_ability_fields():
    return ["strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma", ]


def get_item_fields():
    return [
        "name",
        "description",
        "item_level",
        "gp_cost",
        "activate",
        "frequency",
        "effect"
    ]

set_engine(create_engine('sqlite:///prod.db', connect_args={"check_same_thread": False}, poolclass=StaticPool,
                         echo=True))
