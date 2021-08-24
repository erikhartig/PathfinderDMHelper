from Core.player import Player, AbilityScores, AbilityScore, Skills, SkillScore, get_all_players
from tests.unit_tests.test_dice_roll import all_values_in_results, values_in_bounds


def test_create_player(session):
    player = create_player()
    assert player.ability_scores.strength == 10
    assert player.name == "my_name"


def test_roll_strength(session):
    player = create_player()
    player.ability_scores.strength.roll()


def test_roll_acrobatics(session):
    player = create_player()
    player.skills.acrobatics.roll()


def test_roll_strength_bounds(session):
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


def test_roll_acrobatics_bounds(session):
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
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=10,
        wisdom=10,
        charisma=10
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


def test_get_abilities(session):
    ability_scores = create_ability_scores()
    assert ability_scores.strength == 10
    assert ability_scores.dexterity == 10
    assert ability_scores.constitution == 10
    assert ability_scores.intelligence == 10
    assert ability_scores.wisdom == 10
    assert ability_scores.charisma == 10


def test_get_all_abilities(session):
    expected_dict = {
        "strength": 10,
        "dexterity": 10,
        "constitution": 10,
        "intelligence": 10,
        "wisdom": 10,
        "charisma": 10
    }
    ability_scores = create_ability_scores()
    assert ability_scores.get_all() == expected_dict


def test_ability_persistence(session):
    ability_score = create_ability_scores()
    with session.begin() as db:
        db.add(ability_score)
    with session.begin() as db:
        scores = db.query(AbilityScores)
    all_scores = scores.all()
    specific_score = all_scores[0]
    assert isinstance(specific_score.strength, AbilityScore)


def test_skills_persistence(session):
    skill_score = create_skill_scores()
    with session.begin() as db:
        db.add(skill_score)
    with session.begin() as db:
        scores = db.query(Skills)
    all_scores = scores.all()
    specific_score = all_scores[0]
    assert isinstance(specific_score.thievery, SkillScore)


def test_get_all_skills(session):
    expected_dict = {
        "acrobatics": 0,
        "arcana": 2,
        "athletics": 2,
        "crafting": 2,
        "deception": 2,
        "diplomacy": 2,
        "intimidation": 2,
        "lore": 2,
        "medicine": 2,
        "nature": 2,
        "occultism": 2,
        "performance": 2,
        "religion": 2,
        "society": 3,
        "stealth": 4,
        "survival": 3,
        "thievery": 4
    }
    skill_scores = create_skill_scores()
    assert skill_scores.get_all() == expected_dict


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
