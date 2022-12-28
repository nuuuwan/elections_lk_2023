from elections_lk.core.Election import Election
from elections_lk.core.ElectionType import ElectionType


def main():
    for year in  [1989, 1994, 2000, 2001, 2004, 2010, 2015, 2020]:
        election = Election.init(ElectionType.PARLIAMENTARY, year)
        print(year)
        for party, seats in election.country_result.party_to_seats.items():
            print(f"\t{party}\t{seats}")


if __name__ == '__main__':
    main()
