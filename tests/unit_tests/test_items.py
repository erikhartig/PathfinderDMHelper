from Core.item import Item
from tests.unit_tests.test_player import create_player


def create_sample_item():
    item = Item(
        name="Hat of Disguise",
        description="This ordinary-looking hat allows you to cloak yourself in illusions.",
        activate="1 minute (Interact)",
        frequency="once per day",
        effect="The hat casts a 1st-level illusory disguise spell on you. While setting up the disguise, you can "
               "magically alter the hat to appear as a comb, ribbon, helm, or other piece of headwear.",
        item_level=2,
        gp_cost=30
    )
    return item


def test_get_item_attribute():
    item = create_sample_item()
    assert item.name == "Hat of Disguise"


def test_give_player_item():
    player = create_player()
    item = create_sample_item()
    player.assign_item(item)
    assert item in player.items


def test_give_player_two_items():
    player = create_player()
    first_item = create_sample_item()
    second_item = create_sample_item()
    player.assign_item(first_item)
    player.assign_item(second_item)
    assert first_item in player.items
    assert second_item in player.items


def test_get_player_assigned_to_item():
    player = create_player()
    item = create_sample_item()
    player.assign_item(item)
    assert item.player == player


def test_remove_item_from_player():
    player = create_player()
    item = create_sample_item()
    player.assign_item(item)
    player.remove_item(item)
    assert item not in player.items
    assert item.player is None


def test_remove_item_multiple_items():
    player = create_player()
    first_item = create_sample_item()
    second_item = create_sample_item()
    third_item = create_sample_item()
    player.assign_item(first_item)
    player.assign_item(second_item)
    player.assign_item(third_item)
    player.remove_item(second_item)
    assert first_item in player.items
    assert second_item not in player.items
    assert third_item in player.items
    assert first_item.player == player
    assert second_item.player is None
    assert third_item.player == player
