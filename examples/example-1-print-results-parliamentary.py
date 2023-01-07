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
    year = 2020
    election = ElectionParliamentary.load(year)

    for final_result in election.ed_final_results + [
        election.national_list_final_result
    ]:
        print('-' * 32)
        print(final_result.region_id)
        print('-' * 32)

        for party, votes in final_result.party_to_votes.items_othered(0.01):
            print(party, '\t', humanize(votes))

        print('-' * 8)
        print('valid', '\t', humanize(final_result.summary_statistics.valid))
        print(
            'reje.', '\t', humanize(final_result.summary_statistics.rejected)
        )
        print('poll.', '\t', humanize(final_result.summary_statistics.polled))
        print(
            'elec.', '\t', humanize(final_result.summary_statistics.electors)
        )


if __name__ == '__main__':
    main()
