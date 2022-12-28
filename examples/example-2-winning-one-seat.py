import math
import os

from gig import ents
from matplotlib import pyplot as plt

from elections_lk.core.Election import Election
from elections_lk.core.ElectionType import ElectionType

BASE = 2


def get_gini(x_list):
    s = 0
    total = sum(x_list)
    for x in x_list:
        s += x**2
    return s / (total**2)


def one_seat_parties():
    i = 0
    for year in [1989, 1994, 2000, 2001, 2004, 2010, 2015, 2020]:
        election = Election.init(ElectionType.PARLIAMENTARY, year)
        for party, seats in election.party_to_seats.items():
            if seats in [3, 4, 5]:
                votes = election.country_result.party_to_votes[party]
                p_votes = votes / election.country_result.valid_long
                sources = []

                if party in election.country_result.party_to_seats:
                    party_nl_seats = election.country_result.party_to_seats[
                        party
                    ]
                    source = 'Nat-List'
                    if party_nl_seats > 1:
                        source += f'({party_nl_seats})'
                    sources.append(source)

                ed_votes = []
                for ed_id, ed_result in election.ed_result_idx.items():
                    party_ed_votes = ed_result.party_to_votes.get(party, 0)
                    ed_votes.append(party_ed_votes)
                    # if votes > 0:
                    #     print(f'\t{ed_id} {votes:,}')
                    if party in ed_result.party_to_seats:
                        party_ed_seats = ed_result.party_to_seats[party]
                        ent = ents.get_entity(ed_id)
                        source = ent['name']
                        if party_ed_seats > 1:
                            source += f'({party_ed_seats})'
                        sources.append(source)

                gini = get_gini(ed_votes)
                source_str = ', '.join(sources)
                votes_k = round(votes / 1000.0)
                print(
                    f"{i + 1:>4}) "
                    + f"{year}\t{party}\t{votes_k:,}K"
                    + f"\t{p_votes:.1%}\t{source_str:<20}\t{gini:.2f}"
                )
                i += 1


def get_seats_group(x):
    log_x = math.ceil(math.log(x, BASE))
    max = (int)(BASE**log_x)
    min = (int)(max / BASE + 1)

    if min == max:
        return f'{min}'
    if max > 150:
        return f'{min} -'
    return f'{min} - {max}'


def seat_histogram():
    seats_group_to_n = {}
    for year in [1989, 1994, 2000, 2001, 2004, 2010, 2015, 2020]:
        election = Election.init(ElectionType.PARLIAMENTARY, year)
        for party, seats in election.party_to_seats.items():
            seats_group = get_seats_group(seats)
            if seats_group not in seats_group_to_n:
                seats_group_to_n[seats_group] = 0
            seats_group_to_n[seats_group] += 1

    seat_groups = [
        get_seats_group(BASE**i)
        for i in range(0, (int)(math.log(150, BASE)) + 2)
    ]

    plt.bar(
        seat_groups,
        [seats_group_to_n.get(seat_group, 0) for seat_group in seat_groups],
    )
    plt.title('Sri Lanka - Parliamentary Elections (1989 to 2020)')
    plt.xlabel("Seats for Party")
    plt.ylabel("Number of Parties")

    png_file = __file__ + '.seat_histogram.png'
    fig = plt.gcf()
    fig.set_size_inches(8, 4.5)
    fig.savefig(png_file, dpi=300)
    os.system(f'open -a firefox {png_file}')


if __name__ == '__main__':
    # print('-' * 32)
    # seat_histogram()
    print('-' * 32)
    one_seat_parties()
