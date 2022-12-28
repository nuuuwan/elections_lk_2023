class Seats:
    @staticmethod
    def get_eligible_party_to_votes(party_to_votes, p_limit):
        total_votes = sum(party_to_votes.values())
        limit = total_votes * p_limit
        return dict(
            list(
                filter(
                    lambda x: x[1] >= limit,
                    party_to_votes.items(),
                )
            ),
        )

    @staticmethod
    def assign_nonbonus_seats(party_to_votes, total_seats):
        party_to_non_bonus_seats = {}

        # assign int seats
        total_votes = sum(party_to_votes.values())
        party_to_rem_seats = {}
        all_rem_seats = total_seats
        for party, votes in party_to_votes.items():
            seats_f = votes * total_seats / total_votes
            seats_i = (int)(seats_f)
            party_to_non_bonus_seats[party] = seats_i
            rem_seats = seats_f - seats_i
            party_to_rem_seats[party] = rem_seats
            all_rem_seats -= seats_i

        # assign remainder
        sorted_party_and_rem_seats = sorted(
            party_to_rem_seats.items(),
            key=lambda x: -x[1],
        )
        for i in range(0, all_rem_seats):
            party = sorted_party_and_rem_seats[i][0]
            if party not in party_to_non_bonus_seats:
                party_to_non_bonus_seats[party] = 0
            party_to_non_bonus_seats[party] += 1

        # filter, sort and return
        return dict(
            sorted(
                list(
                    filter(
                        lambda x: x[1] > 0,
                        party_to_non_bonus_seats.items(),
                    )
                ),
                key=lambda x: -x[1],
            )
        )

    @staticmethod
    def get_party_to_seats(total_seats, party_to_votes, p_limit, bonus):
        eligible_party_to_votes = (
            eligible_party_to_votes
        ) = Seats.get_qualified_party_set(party_to_votes, p_limit)
        party_to_non_bonus_seats = Seats.assign_nonbonus_seats(
            eligible_party_to_votes,
            total_seats - bonus,
        )
        return party_to_non_bonus_seats
