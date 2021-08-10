import pytest

from Core.roll_dice import roll_dice, roll_d100, roll_d20, roll_d10, roll_d8, roll_d6, roll_d4


def test_single_roll_in_bounds(bounds=20):
    result = roll_dice(bounds)
    assert result > 0
    assert result < bounds + 1


def all_values_in_results(lower_bound, upper_bound, values):
    for i in range(lower_bound, upper_bound + 1):
        assert i in values


def values_in_bounds(lower_bound, upper_bound, values):
    for res in values:
        assert res in range(lower_bound, upper_bound + 1)


@pytest.mark.parametrize("sides,dice_roller", [(100, roll_d100), (20, roll_d20), (10, roll_d10), (8, roll_d8),
                                               (6, roll_d6), (4, roll_d4)])
def test_roll_dice(sides, dice_roller):
    results = [dice_roller() for _ in range(1000)]
    all_values_in_results(1, sides, results)
    values_in_bounds(1, sides, results)
