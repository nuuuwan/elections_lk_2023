from elections_lk import ElectionLocalAuthority

if __name__ == '__main__':
    election = ElectionLocalAuthority.load(2018)
    print(election.lg_final_results[0])

    print(election.district_final_results[0])

    print(election.country_final_result)

    for (
        party,
        seats,
    ) in election.country_final_result.party_to_seats.items_othered(
        max_p_other=0.02
    ):
        print(party, seats)
