from Core.item import Item


def create_sample_item():
    item = Item(
        name="Hat of Disguise",
        description="This ordinary-looking hat allows you to cloak yourself in illusions.",
        activate="1 minute (Interact)",
        frequency="once per day",
        effect="The hat casts a 1st-level illusory disguise spell on you. While setting up the disguise, you can " \
               "magically alter the hat to appear as a comb, ribbon, helm, or other piece of headwear.",
        item_level=2,
        gp_cost=30
    )
    return item


def test_get_item_attribute():
    item = create_sample_item()
    assert item.name == "Hat of Disguise"
