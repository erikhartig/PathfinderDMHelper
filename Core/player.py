from abc import abstractmethod
from dataclasses import dataclass, field
from math import floor

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, orm
from sqlalchemy.orm import registry, relationship, sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.testing.schema import Table

from Core.roll_dice import roll_d20

mapper_registry = registry()
engine = None
Session = None


def get_session():
    """
    Returns:
        sessionmaker: an object used to construct new sessions
    """
    return Session


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

    def __post_init__(self):
        with get_session().begin() as db:
            db.add(self)


class Scores:
    def get_all(self):
        all_scores = {}
        for score_name, score_value in vars(self).items():
            if isinstance(score_value, Score):
                all_scores[score_name] = score_value
        return all_scores

    def __post_init__(self):
        self.init_on_load()

    @abstractmethod
    def init_on_load(self):
        """
        rebuilds object after sqlalchemy loads it
        """


@mapper_registry.mapped
@dataclass
class AbilityScores(Scores):
    __table__ = Table(
        "ability_scores",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("player_id", Integer, ForeignKey("player.id")),
        Column("strength", Integer),
        Column("dexterity", Integer),
        Column("constitution", Integer),
        Column("intelligence", Integer),
        Column("wisdom", Integer),
        Column("charisma", Integer)
    )
    id: int = field(init=False)
    player_id: int = field(init=False)
    strength: AbilityScore or int = AbilityScore(10)
    dexterity: AbilityScore or int = AbilityScore(10)
    constitution: AbilityScore or int = AbilityScore(10)
    intelligence: AbilityScore or int = AbilityScore(10)
    wisdom: AbilityScore or int = AbilityScore(10)
    charisma: AbilityScore or int = AbilityScore(10)

    @orm.reconstructor
    def init_on_load(self):
        annos = self.__annotations__
        for score_name, score_value in vars(self).items():
            if score_name in annos and annos[score_name] is AbilityScore and not isinstance(score_value, Score):
                self.__setattr__(score_name, AbilityScore(score_value))


@mapper_registry.mapped
@dataclass
class Skills (Scores):
    __table__ = Table(
        "skills",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("player_id", Integer, ForeignKey("player.id")),
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
    )
    id: int = field(init=False)
    player_id: int = field(init=False)
    acrobatics: SkillScore = SkillScore(0)
    arcana: SkillScore = SkillScore(0)
    athletics: SkillScore = SkillScore(0)
    crafting: SkillScore = SkillScore(0)
    deception: SkillScore = SkillScore(0)
    diplomacy: SkillScore = SkillScore(0)
    intimidation: SkillScore = SkillScore(0)
    lore: SkillScore = SkillScore(0)
    medicine: SkillScore = SkillScore(0)
    nature: SkillScore = SkillScore(0)
    occultism: SkillScore = SkillScore(0)
    performance: SkillScore = SkillScore(0)
    religion: SkillScore = SkillScore(0)
    society: SkillScore = SkillScore(0)
    stealth: SkillScore = SkillScore(0)
    survival: SkillScore = SkillScore(0)
    thievery: SkillScore = SkillScore(0)

    @orm.reconstructor
    def init_on_load(self):
        annos = self.__annotations__
        for score_name, score_value in vars(self).items():
            if score_name in annos and annos[score_name] is SkillScore and not isinstance(score_value, Score):
                self.__setattr__(score_name, SkillScore(score_value))


@mapper_registry.mapped
@dataclass
class Player:
    __tablename__ = "player"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(default=None, metadata={"sa": Column(String(50))})
    ability_scores: AbilityScores = field(
        default=AbilityScores(), metadata={"sa": relationship("AbilityScores", uselist=False)}
    )
    skills: Skills = field(default=Skills(), metadata={"sa": relationship("Skills", uselist=False)})
    items: list = field(default_factory=list, metadata={"sa": relationship("Item", backref="player")})

    def __post_init__(self):
        with get_session().begin() as db:
            db.add(self)

    def add_item(self, item):
        with get_session().begin() as db:
            db.add(self)
            self.items.append(item)

    def remove_item(self, item):
        with get_session().begin() as db:
            db.add(self)
            self.items.remove(item)


def get_all_players():
    with get_session().begin() as db:
        players = db.query(Player)
    return players.all()


def get_all_items():
    with get_session().begin() as db:
        items = db.query(Item)
    return items.all()


set_engine(create_engine('sqlite:///prod.db', connect_args={"check_same_thread": False}, poolclass=StaticPool,
                         echo=True))
