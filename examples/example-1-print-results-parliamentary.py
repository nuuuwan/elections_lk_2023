from elections_lk.core.ElectionParliamentary import ElectionParliamentary
from elections_lk.core.StrToInt import StrToInt
MIN_P_VOTES = 0.01

def humanize(x):
    if x > 1_000_000:
        return f'{x / 1_000_000:.0f}M'
    if x > 1_000:
        return f'{x / 1_000:.0f}K'
    return f'{x:,}'

def main():
    year = 2020
    election = ElectionParliamentary.load(year)
    for pd_result in election.pd_results:
        print(pd_result.region_id)
        valid = pd_result.summary_statistics.valid
        for party, votes in pd_result.party_to_votes.items_othered(0.05):
            p_votes = votes / valid
            votes_str = humanize(votes)
            print(f'\t{party}\t{votes_str}\t({p_votes:.0%})')
        print('-' * 32)

    for ed_final_result in election.ed_final_results:
        print(ed_final_result.region_id)
        valid = ed_final_result.summary_statistics.valid
        for party, votes in ed_final_result.party_to_votes.items_othered(0.025):
            p_votes = votes / valid
            votes_str = humanize(votes)
            seats = ed_final_result.party_to_seats[party] if party != StrToInt.OTHERS else 0
            print(f'\t{party}\t{votes_str}\t({p_votes:.0%})\t{seats}')
        print('-' * 32)

    print('National List')
    valid = election.national_list_final_result.summary_statistics.valid
    for party, votes in election.national_list_final_result.party_to_votes.items_othered(0.005):
        p_votes = votes / valid
        votes_str = humanize(votes)
        seats = election.country_final_result.party_to_seats[party] if party != StrToInt.OTHERS else 0
        print(f'\t{party}\t{votes_str}\t({p_votes:.0%})\t{seats}')
    print('-' * 32)

    print('Country Final')
    valid = election.country_final_result.summary_statistics.valid
    for party, votes in election.country_final_result.party_to_votes.items_othered(0.005):
        p_votes = votes / valid
        votes_str = humanize(votes)
        seats = election.country_final_result.party_to_seats[party] if party != StrToInt.OTHERS else 0
        print(f'\t{party}\t{votes_str}\t({p_votes:.0%})\t{seats}')
    print('-' * 32)




if __name__ == '__main__':
    main()
