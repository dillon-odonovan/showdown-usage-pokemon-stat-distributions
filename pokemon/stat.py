from .nature import Nature, NATURE_MODIFIERS
from enum import Enum
from math import floor

LEVEL_FIFTY = 50
MAX_INDIVIDUAL_VALUE = 31
MIN_INDIVIDUAL_VALUE = 0


class Stat(Enum):
    HP = 1
    ATTACK = 2
    DEFENSE = 3
    SPECIAL_ATTACK = 4
    SPECIAL_DEFENSE = 5
    SPEED = 6


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
