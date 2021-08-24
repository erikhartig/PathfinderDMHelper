import pytest

from Core.scrape import request_item_data, get_item_names


def test_get_item_1():
    item_info = request_item_data(1)
    assert item_info["name"] == "Adventurer's Pack"
    assert item_info["item_level"] == 0
    assert item_info["gp_cost"] == 1.5
    assert item_info["description"] == "This item is the starter kit for an adventurer, containing the essential " \
                                       "items for exploration and survival. The Bulk value is for the entire pack " \
                                       "together, but see the descriptions of individual items as necessary. The " \
                                       "pack contains the following items: backpack (containing the other goods)," \
                                       " bedroll, 10 pieces of chalk, flint and steel, 50 feet of rope, 2 weeks' " \
                                       "rations, soap, 5 torches, and a waterskin."


def test_get_item_2():
    item_info = request_item_data(2)
    assert item_info["name"] == "Alchemist's Tools"
    assert item_info["item_level"] == 0
    assert item_info["gp_cost"] == 3
    assert item_info["description"] == "This mobile collection of vials and chemicals can be used for simple " \
                                       "alchemical tasks. If you wear your alchemist's tools, you can draw and " \
                                       "replace them as part of the action that uses them."


def test_get_item_3():
    item_info = request_item_data(3, "Artisan's Tools")
    assert item_info["name"] == "Artisan's Tools"
    assert item_info["item_level"] == 0
    assert item_info["gp_cost"] == 4
    assert item_info["description"] == "You need these tools to create items from raw materials with the Craft skill." \
                                       " Different sets are needed for different work, as determined by the GM; for " \
                                       "example, blacksmith's tools differ from woodworker's tools. If you wear your " \
                                       "artisan's tools, you can draw and replace them as part of the action that " \
                                       "uses them."


def test_get_item_3_subitem():
    item_info = request_item_data(3, "Artisan's Tools (Sterling)")
    assert item_info["name"] == "Artisan's Tools (Sterling)"
    assert item_info["item_level"] == 3
    assert item_info["gp_cost"] == 50
    assert item_info["description"] == "You need these tools to create items from raw materials with the Craft skill." \
                                       " Different sets are needed for different work, as determined by the GM; for " \
                                       "example, blacksmith's tools differ from woodworker's tools. If you wear your " \
                                       "artisan's tools, you can draw and replace them as part of the action that " \
                                       "uses them. Sterling artisan's tools give you a +1 item bonus to the check."


def test_get_hat_of_disguise():
    item_info = request_item_data(442, "Hat of Disguise")
    assert item_info["name"] == "Hat of Disguise"
    assert item_info["item_level"] == 2
    assert item_info["gp_cost"] == 30
    assert item_info["description"] == "This ordinary-looking hat allows you to cloak yourself in illusions."
    assert item_info["activate"] == "1 minute (Interact)"
    assert item_info["frequency"] == "once per day"
    assert item_info["effect"] == "The hat casts a 1st-level illusory disguise spell on you. While setting up the " \
                                  "disguise, you can magically alter the hat to appear as a comb, ribbon, helm, or " \
                                  "other piece of headwear."


def test_invalid_name_raise_error():
    with pytest.raises(ValueError):
        request_item_data(442, "Hat of Disgose")


def test_get_item_names():
    names = get_item_names()
    assert len(names) == 967
    for link in names.values():
        assert link.isdecimal()
