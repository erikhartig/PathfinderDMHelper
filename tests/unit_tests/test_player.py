from Core.player import Player, get_all_players
from tests.unit_tests.test_dice_roll import all_values_in_results, values_in_bounds


def test_create_player(session):
    player = create_player()
    assert player.strength == 10
    assert player.name == "my_name"


def test_roll_strength(session):
    player = create_player()
    player.strength.roll()


def test_roll_acrobatics(session):
    player = create_player()
    player.acrobatics.roll()


def test_roll_strength_bounds(session):
    player = create_player()
    results = [player.strength.roll() for _ in range(1000)]
    all_values_in_results(1, 20, results)
    values_in_bounds(1, 20, results)

    player.strength.set(14)
    results = [player.strength.roll() for _ in range(1000)]
    all_values_in_results(3, 22, results)
    values_in_bounds(3, 22, results)

    player.strength.set(15)
    results = [player.strength.roll() for _ in range(1000)]
    all_values_in_results(3, 22, results)
    values_in_bounds(3, 22, results)

    player.strength.set(6)
    results = [player.strength.roll() for _ in range(1000)]
    all_values_in_results(0, 18, results)
    values_in_bounds(0, 18, results)


def test_roll_acrobatics_bounds(session):
    player = create_player()
    results = [player.acrobatics.roll() for _ in range(1000)]
    all_values_in_results(1, 20, results)
    values_in_bounds(1, 20, results)

    player.acrobatics.set(2)
    results = [player.acrobatics.roll() for _ in range(1000)]
    all_values_in_results(3, 22, results)
    values_in_bounds(3, 22, results)

    player.acrobatics.set(3)
    results = [player.acrobatics.roll() for _ in range(1000)]
    all_values_in_results(4, 23, results)
    values_in_bounds(4, 23, results)

    player.acrobatics.set(-2)
    results = [player.acrobatics.roll() for _ in range(1000)]
    all_values_in_results(0, 18, results)
    values_in_bounds(0, 18, results)


def create_player():
    return Player(name="my_name",
                  strength=10,
                  dexterity=10,
                  constitution=10,
                  intelligence=10,
                  wisdom=10,
                  charisma=10,
                  acrobatics=0,
                  arcana=2,
                  athletics=2,
                  crafting=2,
                  deception=2,
                  diplomacy=2,
                  intimidation=2,
                  lore=2,
                  medicine=2,
                  nature=2,
                  occultism=2,
                  performance=2,
                  religion=2,
                  society=3,
                  stealth=4,
                  survival=3,
                  thievery=4
                  )


def test_get_abilities(session):
    player = create_player()
    assert player.strength == 10
    assert player.dexterity == 10
    assert player.constitution == 10
    assert player.intelligence == 10
    assert player.wisdom == 10
    assert player.charisma == 10


def test_persistence(session):
    player_obj = create_player()
    with session.begin() as db:
        players = db.query(Player)
    assert player_obj in players


def test_get_all_players(session):
    player_1 = create_player()
    player_2 = create_player()
    players = get_all_players()
    assert player_1 in players
    assert player_2 in players
    assert players == [player_1, player_2]


def test_get_all_players_no_players(session):
    players = get_all_players()
    assert players == []
