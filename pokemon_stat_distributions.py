from collections import Counter
import ijson
from os import makedirs
from os.path import dirname, exists
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
}
TPS = 100


def create_file(stats_dir: str, pokemon_name: str, pokemon_stat_distribution: dict[Stat, Counter[int, int]], num: int):
    output_filename = f'{stats_dir}/out/{pokemon_name}.txt'
    makedirs(dirname(output_filename), exist_ok=True)
    with open(output_filename, 'w') as f:
        f.write(f'{pokemon_name}\n\n')
        for stat, stat_value_counts in pokemon_stat_distribution.items():
            f.write(f'{stat.name}\n')
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
                f.write(f'{stat_value}  ||  {count / num:.3f}\n')
                cumulative_count += count
                cumulative_tuples.append((stat_value, cumulative_count))
            f.write('\n')
            f.write(f'{stat.name} - Cumulative\n')
            for c in cumulative_tuples:
                f.write(f'{c[0]}  ||  {c[1] / num:.3f}\n')
            f.write('\n')


def normalize_pokemon_name(pokemon_name: str) -> str:
    return pokemon_name.lower().replace(' ', '-')


def main():
    stats_dir = './stats/2023-01/gen9vgc2023series2-1630'  # TODO: make dynamic
    stats_file = 'gen9vgc2023series2-1630.json'  # TODO: make file dynamic
    with open(f'{stats_dir}/{stats_file}', 'rb') as f:
        for pokemon_name, pokemon_stats in ijson.kvitems(f, 'data'):
            normalized_pokemon_name = normalize_pokemon_name(str(pokemon_name))

            pokebase_pokemon_name = POKEBASE_NORMALIZED_POKEMON_NAMES[normalized_pokemon_name] \
                if normalized_pokemon_name in POKEBASE_NORMALIZED_POKEMON_NAMES \
                else normalized_pokemon_name

            pokemon = pokebase.pokemon(pokebase_pokemon_name)
            spreads = pokemon_stats['Spreads']

            pokemon_stat_distribution = {
                Stat.HP: Counter(),
                Stat.ATTACK: Counter(),
                Stat.DEFENSE: Counter(),
                Stat.SPECIAL_ATTACK: Counter(),
                Stat.SPECIAL_DEFENSE: Counter(),
                Stat.SPEED: Counter(),
            }

            for spread in spreads:
                parsed_spread = Spread(spread)

                for (stat, effort_values) in parsed_spread.effort_values.items():
                    stat_index = stat.value - 1
                    base_stat = pokemon.stats[stat_index].base_stat

                    stat_at_lv_50 = calc_stat_at_lv_50(
                        stat, base_stat, effort_values, parsed_spread.nature)

                    pokemon_stat_distribution[stat][stat_at_lv_50] += 1

            create_file(stats_dir,
                        normalized_pokemon_name,
                        pokemon_stat_distribution, len(spreads))

            sleep(1 / TPS)


if __name__ == '__main__':
    main()
