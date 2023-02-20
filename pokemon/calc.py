from .nature import Nature
from .stat import Stat
from math import floor

LEVEL_FIFTY = 50
MAX_INDIVIDUAL_VALUE = 31
MIN_INDIVIDUAL_VALUE = 0
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


def _calc_hp_stat(base_stat: int, effort_values: int, level: int):
    return floor(((2 * base_stat + MAX_INDIVIDUAL_VALUE +
                   effort_values / 4 + 100) * level) / 100 + 10)


def _calc_non_hp_stat(base_stat: int, effort_values: int, stat: Stat, nature: Nature, level: int):
    nature_modifier = NATURE_MODIFIERS.get(nature).get(stat, 1)
    individual_value = MIN_INDIVIDUAL_VALUE if nature_modifier < 1 else MAX_INDIVIDUAL_VALUE

    return floor((((2 * base_stat + individual_value + effort_values / 4)
                   * level) / 100 + 5) * nature_modifier)


def _calc_stat(stat: Stat, base_stat: int, effort_values: int, nature: Nature, level: int):
    if stat == Stat.HP:
        return _calc_hp_stat(base_stat, effort_values, level)
    return _calc_non_hp_stat(base_stat, effort_values, stat, nature, level)


def calc_stat_at_lv_50(stat: Stat, base_stat: int, effort_values: int, nature: Nature):
    return _calc_stat(stat, base_stat, effort_values, nature, LEVEL_FIFTY)
