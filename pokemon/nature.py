from enum import Enum
from .stat import Stat


class Nature(Enum):
    HARDY = 1
    LONELY = 2
    BRAVE = 3
    ADAMANT = 4
    NAUGHTY = 5
    BOLD = 6
    DOCILE = 7
    RELAXED = 8
    IMPISH = 9
    LAX = 10
    TIMID = 11
    HASTY = 12
    SERIOUS = 13
    JOLLY = 14
    NAIVE = 15
    MODEST = 16
    MILD = 17
    QUIET = 18
    BASHFUL = 19
    RASH = 20
    CALM = 21
    GENTLE = 22
    SASSY = 23
    CAREFUL = 24
    QUIRKY = 25


NATURE_MODIFIERS: dict[Nature, dict[Stat, float]] = {
    Nature.HARDY: {},
    Nature.LONELY: {Stat.ATTACK: 1.1, Stat.DEFENSE: 0.9},
    Nature.BRAVE: {Stat.ATTACK: 1.1, Stat.SPEED: 0.9},
    Nature.ADAMANT: {Stat.ATTACK: 1.1, Stat.SPECIAL_ATTACK: 0.9},
    Nature.NAUGHTY: {Stat.ATTACK: 1.1, Stat.SPECIAL_DEFENSE: 0.9},
    Nature.BOLD: {Stat.DEFENSE: 1.1, Stat.ATTACK: 0.9},
    Nature.DOCILE: {},
    Nature.RELAXED: {Stat.DEFENSE: 1.1, Stat.SPEED: 0.9},
    Nature.IMPISH: {Stat.DEFENSE: 1.1, Stat.SPECIAL_ATTACK: 0.9},
    Nature.LAX: {Stat.DEFENSE: 1.1, Stat.SPECIAL_DEFENSE: 0.9},
    Nature.TIMID: {Stat.SPEED: 1.1, Stat.ATTACK: 0.9},
    Nature.HASTY: {Stat.SPEED: 1.1, Stat.DEFENSE: 0.9},
    Nature.SERIOUS: {},
    Nature.JOLLY: {Stat.SPEED: 1.1, Stat.SPECIAL_ATTACK: 0.9},
    Nature.NAIVE: {Stat.SPEED: 1.1, Stat.SPECIAL_DEFENSE: 0.9},
    Nature.MODEST: {Stat.SPECIAL_ATTACK: 1.1, Stat.ATTACK: 0.9},
    Nature.MILD: {Stat.SPECIAL_ATTACK: 1.1, Stat.DEFENSE: 0.9},
    Nature.QUIET: {Stat.SPECIAL_ATTACK: 1.1, Stat.SPEED: 0.9},
    Nature.BASHFUL: {},
    Nature.RASH: {Stat.SPECIAL_ATTACK: 1.1, Stat.SPECIAL_DEFENSE: 0.9},
    Nature.CALM: {Stat.SPECIAL_DEFENSE: 1.1, Stat.ATTACK: 0.9},
    Nature.GENTLE: {Stat.SPECIAL_DEFENSE: 1.1, Stat.DEFENSE: 0.9},
    Nature.SASSY: {Stat.SPECIAL_DEFENSE: 1.1, Stat.SPEED: 0.9},
    Nature.CAREFUL: {Stat.SPECIAL_DEFENSE: 1.1, Stat.ATTACK: 0.9},
    Nature.QUIRKY: {}
}
