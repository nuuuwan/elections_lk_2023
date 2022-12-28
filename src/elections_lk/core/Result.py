from dataclasses import dataclass


@dataclass
class Result:
    region_id: str
    valid: int
    rejected: int
    polled: int
    electors: int
    party_to_votes: dict
    seats: int
    party_to_seats: dict

    @property
    def p_rejected(self):
        return self.rejected / self.polled

    @property
    def p_valid(self):
        return self.valid / self.polled

    @property
    def p_turnout(self):
        return self.polled / self.electors

    @property
    def valid_long(self):
        return sum(self.party_to_votes.values())

    def get_party_votes(self, party):
        return self.party_to_votes[party]

    def get_party_votes_p(self, party):
        return self.get_party_votes(party) / self.valid

    @staticmethod
    def concat(concat_region_id, result_list):
        valid = sum([r.valid for r in result_list])
        rejected = sum([r.rejected for r in result_list])
        polled = sum([r.polled for r in result_list])
        electors = sum([r.electors for r in result_list])
        party_to_votes = {}
        for r in result_list:
            for k, v in r.party_to_votes.items():
                if k not in party_to_votes:
                    party_to_votes[k] = 0
                party_to_votes[k] += v

        seats = sum([r.seats for r in result_list])
        party_to_seats = {}
        for r in result_list:
            for k, v in r.party_to_seats.items():
                if k not in party_to_seats:
                    party_to_seats[k] = 0
                party_to_seats[k] += v

        return Result(
            concat_region_id,
            valid,
            rejected,
            polled,
            electors,
            party_to_votes,
            seats,
            party_to_seats,
        )
