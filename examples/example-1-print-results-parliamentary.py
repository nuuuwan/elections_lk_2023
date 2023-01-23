from elections_lk.elections import ElectionParliamentary

MIN_P_VOTES = 0.01


def humanize(x):
    # if x > 1_000_000:
    #     return f'{x / 1_000_000:.2f}M'
    # if x > 100_000:
    #     return f'{x / 1_000:.0f}K'
    # if x > 10_000:
    #     return f'{x / 1_000:.1f}K'
    # if x > 1_000:
    #     return f'{x / 1_000:.2f}K'
    return f'{x:,}'


def main():
    for year in [2000]:
        print('-' * 32)
        print(year)
        print('-' * 32)
        election = ElectionParliamentary.load(year)
        for result in election.pd_results + [election.ed_final_results[10]]:
            if result.region_id[:5] != 'EC-11':
                continue
            print('-' * 32)
            print(result.region_id)
            for party, votes in result.party_to_votes.items_othered(0.005):
                print('\t'.join([party, humanize(votes)]))


if __name__ == '__main__':
    main()
