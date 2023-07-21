from collections import Counter
import ijson
from os import makedirs
from os.path import dirname
import pokebase
from pokemon.calc import calc_stat_at_lv_50
from pokemon.stat import Stat
from pokemon.spread import Spread
from time import sleep

POKEBASE_NORMALIZED_POKEMON_NAMES = {
    'basculin': 'basculin-red-striped',
    'eiscue': 'eiscue-ice',
    'indeedee-f': 'indeedee-female',
    'lycanroc': 'lycanroc-midday',
    'indeedee': 'indeedee-male',
    'mimikyu': 'mimikyu-disguised',
    'oinkologne-f': 'oinkologne-female',
    'oricorio': 'oricorio-baile',
    'oricorio-pa\'u': 'oricorio-pau',
    'tauros-paldea-aqua': 'tauros-paldea-aqua-breed',
    'tauros-paldea-blaze': 'tauros-paldea-blaze-breed',
    'tauros-paldea-combat': 'tauros-paldea-combat-breed',
    'toxtricity': 'toxtricity-amped',
    'tornadus': 'tornadus-incarnate',
    'thundurus': 'tornadus-incarnate',
    'landorus': 'landorus-incarnate',
    'enamorus': 'enamorus-incarnate',
    'urshifu': 'urshifu-single-strike',
    'basculegion': 'basculegion-male',
    'basculegion-f': 'basculegion-female',
}
TPS = 100
PHYSICAL_BULK = 'Physical Bulk'
SPECIAL_BULK = 'Special Bulk'


def create_file(stats_dir: str, pokemon_name: str, pokemon_stat_distribution: dict[str, Counter[int, int]], num: int):
    output_filename = f'{stats_dir}/out/{pokemon_name}.txt'
    makedirs(dirname(output_filename), exist_ok=True)
    with open(output_filename, 'w') as f:
        f.write(f'{pokemon_name}\n\n')
        for stat, stat_value_counts in pokemon_stat_distribution.items():
            f.write(f'{stat}\n')
            sorted_counts = [(key, val) for key, val in sorted(
                stat_value_counts.items(), key=lambda item: item[0])]
            index = 0
            cumulative_count = 0
            cumulative_tuples = []
            min_stat_value = sorted_counts[0][0]
            max_stat_value = sorted_counts[-1][0]
            for stat_value in range(min_stat_value, max_stat_value + 1):
                count = 0
                occurring_stat_value = sorted_counts[index][0]
                if stat_value == occurring_stat_value:
                    count = sorted_counts[index][1]
                    index += 1
                f.write(f'{stat_value},{count / num:.3f}\n')
                cumulative_count += count
                cumulative_tuples.append((stat_value, cumulative_count))
            f.write('\n')
            f.write(f'{stat} - Cumulative\n')
            for c in cumulative_tuples:
                f.write(f'{c[0]},{c[1] / num:.3f}\n')
            f.write('\n')


def normalize_pokemon_name(pokemon_name: str) -> str:
    return pokemon_name.lower().replace(' ', '-')


def main():
    stats = 'stats'  # TODO: make dynamic
    month = '2023-06'
    metagame_rating = 'gen9vgc2023regulationd-1630'  # TODO: make file dynamic
    with open(f'./{stats}/{month}/{metagame_rating}/{metagame_rating}.json', 'rb') as f:
        for pokemon_name, pokemon_stats in ijson.kvitems(f, 'data'):
            normalized_pokemon_name = normalize_pokemon_name(str(pokemon_name))

            pokebase_pokemon_name = POKEBASE_NORMALIZED_POKEMON_NAMES[normalized_pokemon_name] \
                if normalized_pokemon_name in POKEBASE_NORMALIZED_POKEMON_NAMES \
                else normalized_pokemon_name

            pokemon = pokebase.pokemon(pokebase_pokemon_name)
            spreads = pokemon_stats['Spreads']

            pokemon_stat_distribution = {
                Stat.HP.name: Counter(),
                Stat.ATTACK.name: Counter(),
                Stat.DEFENSE.name: Counter(),
                Stat.SPECIAL_ATTACK.name: Counter(),
                Stat.SPECIAL_DEFENSE.name: Counter(),
                Stat.SPEED.name: Counter(),
                PHYSICAL_BULK: Counter(),
                SPECIAL_BULK: Counter(),
            }

            spread_weighting_sum = 0

            for spread in spreads:
                parsed_spread = Spread(spread)

                pokemon_stats = {}

                for (stat, effort_values) in parsed_spread.effort_values.items():
                    stat_index = stat.value - 1
                    base_stat = pokemon.stats[stat_index].base_stat

                    stat_at_lv_50 = calc_stat_at_lv_50(
                        stat, base_stat, effort_values, parsed_spread.nature)

                    pokemon_stats[stat.name] = stat_at_lv_50

                pokemon_stats[PHYSICAL_BULK] = pokemon_stats[Stat.HP.name] * \
                    pokemon_stats[Stat.DEFENSE.name]
                pokemon_stats[SPECIAL_BULK] = pokemon_stats[Stat.HP.name] * \
                    pokemon_stats[Stat.SPECIAL_DEFENSE.name]

                spread_weighting = spreads[spread]
                spread_weighting_sum += spread_weighting

                for (stat, value) in pokemon_stats.items():
                    pokemon_stat_distribution[stat][value] += spread_weighting

            create_file(f'{stats}/{month}/{metagame_rating}',
                        normalized_pokemon_name,
                        pokemon_stat_distribution, spread_weighting_sum)

            sleep(1 / TPS)


if __name__ == '__main__':
    main()
