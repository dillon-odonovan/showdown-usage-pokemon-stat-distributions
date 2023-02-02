from .nature import Nature
from .stat import Stat


class Spread():
    # Hardy:4/0/108/116/68/212
    def __init__(self, spread: str) -> None:
        spread_parts = spread.split(':')
        self.nature = Nature[spread_parts[0].upper()]

        stat_parts = spread_parts[1].split('/')
        self.effort_values = {
            Stat.HP: int(stat_parts[0]),
            Stat.ATTACK: int(stat_parts[1]),
            Stat.DEFENSE: int(stat_parts[2]),
            Stat.SPECIAL_ATTACK: int(stat_parts[3]),
            Stat.SPECIAL_DEFENSE: int(stat_parts[4]),
            Stat.SPEED: int(stat_parts[5])
        }
