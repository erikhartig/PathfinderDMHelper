import random


def roll_dice(sides):
    return random.randrange(1, sides + 1)


def roll_d100():
    return roll_dice(100)


def roll_d20():
    return roll_dice(20)


def roll_d10():
    return roll_dice(10)


def roll_d8():
    return roll_dice(8)


def roll_d6():
    return roll_dice(6)


def roll_d4():
    return roll_dice(4)
