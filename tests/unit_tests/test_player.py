from Core.player import Player, AbilityScores, AbilityScore, Skills, SkillScore
from tests.unit_tests.test_dice_roll import all_values_in_results, values_in_bounds


def test_create_player():
    player = create_player()
    assert player.ability_scores.strength() == 10
    assert player.name == "my_name"


def test_roll_strength():
    player = create_player()
    player.ability_scores.strength.roll()


def test_roll_acrobatics():
    player = create_player()
    player.skills.acrobatics.roll()


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


def test_roll_acrobatics_bounds():
    player = create_player()
    results = [player.skills.acrobatics.roll() for _ in range(1000)]
    all_values_in_results(1, 20, results)
    values_in_bounds(1, 20, results)

    player.skills.acrobatics.set(2)
    results = [player.skills.acrobatics.roll() for _ in range(1000)]
    all_values_in_results(3, 22, results)
    values_in_bounds(3, 22, results)

    player.skills.acrobatics.set(3)
    results = [player.skills.acrobatics.roll() for _ in range(1000)]
    all_values_in_results(4, 23, results)
    values_in_bounds(4, 23, results)

    player.skills.acrobatics.set(-2)
    results = [player.skills.acrobatics.roll() for _ in range(1000)]
    all_values_in_results(0, 18, results)
    values_in_bounds(0, 18, results)


def create_player():
    ability_scores = create_ability_scores()
    skills = create_skill_scores()
    return Player("my_name", ability_scores, skills)


def create_ability_scores():
    return AbilityScores(
        strength=AbilityScore(10),
        dexterity=AbilityScore(10),
        constitution=AbilityScore(10),
        intelligence=AbilityScore(10),
        wisdom=AbilityScore(10),
        charisma=AbilityScore(10)
    )


def create_skill_scores():
    return Skills(
        acrobatics=SkillScore(0),
        arcana=SkillScore(2),
        athletics=SkillScore(2),
        crafting=SkillScore(2),
        deception=SkillScore(2),
        diplomacy=SkillScore(2),
        intimidation=SkillScore(2),
        lore=SkillScore(2),
        medicine=SkillScore(2),
        nature=SkillScore(2),
        occultism=SkillScore(2),
        performance=SkillScore(2),
        religion=SkillScore(2),
        society=SkillScore(3),
        stealth=SkillScore(4),
        survival=SkillScore(3),
        thievery=SkillScore(4)

    )


def test_get_abilities():
    ability_scores = create_ability_scores()
    assert ability_scores.strength() == 10
    assert ability_scores.dexterity() == 10
    assert ability_scores.constitution() == 10
    assert ability_scores.intelligence() == 10
    assert ability_scores.wisdom() == 10
    assert ability_scores.charisma() == 10
