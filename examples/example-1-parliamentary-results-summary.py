from elections_lk.core.Election import Election
from elections_lk.core.ElectionType import ElectionType


def summary_by_party(election):
    result = election.country_result
    for party, seats in result.party_to_seats.items():
        votes = result.party_to_votes[party]
        print(f"\t{party}\t{seats:>4}\t{votes:>8}")


def summary_by_ed(election):
    for ed_id, result in sorted(
        election.ed_result_idx.items(), key=lambda x: x[0]
    ):
        print(f"\t{ed_id}\t{result.valid:>8}")


def summary_for_year(year):
    election = Election.init(ElectionType.PARLIAMENTARY, year)
    print('-' * 32)
    print(year)
    print('-' * 32)
    summary_by_party(election)
    # print('.' * 32)
    # summary_by_ed(election)


def main():
    for year in [1989, 1994, 2000, 2001, 2004, 2010, 2015, 2020]:
        summary_for_year(year)


if __name__ == '__main__':
    main()
