from Core.player import Player, AbilityScores, AbilityScore
from tests.unit_tests.test_dice_roll import all_values_in_results, values_in_bounds


def test_create_player():
    player = create_player()
    assert player.ability_scores.strength() == 10
    assert player.name == "my_name"


def test_roll_strength():
    player = create_player()
    player.ability_scores.strength.roll()


def test_roll_strength_bounds():
    player = create_player()
    results = [player.ability_scores.strength.roll() for _ in range(1000)]
    all_values_in_results(1, 20, results)
    values_in_bounds(1, 20, results)

    player.ability_scores.strength.set(14)
    results = [player.ability_scores.strength.roll() for _ in range(1000)]
    all_values_in_results(3, 22, results)
    values_in_bounds(3, 22, results)

    player.ability_scores.strength.set(15)
    results = [player.ability_scores.strength.roll() for _ in range(1000)]
    all_values_in_results(3, 22, results)
    values_in_bounds(3, 22, results)

    player.ability_scores.strength.set(6)
    results = [player.ability_scores.strength.roll() for _ in range(1000)]
    all_values_in_results(0, 18, results)
    values_in_bounds(0, 18, results)


def create_player():
    ability_scores = create_ability_scores()
    return Player("my_name", ability_scores)


def create_ability_scores():
    return AbilityScores(
        strength=AbilityScore(10),
        dexterity=AbilityScore(10),
        constitution=AbilityScore(10),
        intelligence=AbilityScore(10),
        wisdom=AbilityScore(10),
        charisma=AbilityScore(10)
    )


def test_get_abilities():
    ability_scores = create_ability_scores()
    assert ability_scores.strength() == 10
    assert ability_scores.dexterity() == 10
    assert ability_scores.constitution() == 10
    assert ability_scores.intelligence() == 10
    assert ability_scores.wisdom() == 10
    assert ability_scores.charisma() == 10
