from Core.player import Item, get_all_items
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


def test_item_minimal_fields(session):
    Item(
        name="Aeon Stone, Clear Spindle",
        description="This aeon stone sustains you by negating the need for food or water.",
        item_level=1,
        gp_cost=245
    )


def test_get_item_attribute(session):
    item = create_sample_item()
    assert item.name == "Hat of Disguise"


def test_give_player_item(session):
    player = create_player()
    item = create_sample_item()
    with session.begin() as db:
        db.add(item)
        player.items.append(item)
    assert item in player.items
    assert item.player_id == player.id


def test_give_player_two_items(session):
    player = create_player()
    first_item = create_sample_item()
    second_item = create_sample_item()
    player.add_item(first_item)
    player.add_item(second_item)
    assert first_item in player.items
    assert second_item in player.items
    assert first_item.player_id == player.id
    assert second_item.player_id == player.id


def test_get_player_assigned_to_item(session):
    player = create_player()
    item = create_sample_item()
    player.add_item(item)
    assert item.player == player


def test_remove_item_from_player(session):
    player = create_player()
    item = create_sample_item()
    player.add_item(item)
    assert item.player_id == player.id
    player.remove_item(item)
    assert item not in player.items
    assert item.player_id is None


def test_remove_item_multiple_items(session):
    player = create_player()
    first_item = create_sample_item()
    second_item = create_sample_item()
    third_item = create_sample_item()

    player.add_item(first_item)
    player.add_item(second_item)
    player.add_item(third_item)

    player.remove_item(second_item)
    assert first_item in player.items
    assert second_item not in player.items
    assert third_item in player.items
    assert first_item.player_id == player.id
    assert second_item.player_id is None
    assert third_item.player_id == player.id


def test_get_all_items(session):
    item_1 = create_sample_item()
    item_2 = create_sample_item()
    items = get_all_items()
    assert item_1 in items
    assert item_2 in items
    assert items == [item_1, item_2]


def test_get_item_fields(session):
    item = create_sample_item()
    item_fields = item.get_fields()
    assert set(item_fields.keys()) == \
           {"name", "description", "activate", "frequency", "effect", "item_level", "gp_cost"}
