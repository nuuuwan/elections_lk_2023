from dataclasses import dataclass

NON_PARTY_FIELDS = ['entity_id', 'valid', 'rejected', 'polled', 'electors']


def parse_int(x):
    return (int)((float)(x))


@dataclass
class Result:
    region_id: str
    valid: int
    rejected: int
    polled: int
    electors: int
    party_to_votes: dict

    @property
    def p_rejected(self):
        return self.rejected / self.polled

    @property
    def p_valid(self):
        return self.valid / self.polled

    @property
    def p_turnout(self):
        return self.polled / self.electors

    def get_party_votes(self, party):
        return self.party_to_votes[party]

    def get_party_votes_p(self, party):
        return self.get_party_votes(party) / self.valid

    @staticmethod
    def extractPartyToVotes(d):
        party_to_votes = {}
        for k, v in d.items():
            if k not in NON_PARTY_FIELDS:
                party_to_votes[k] = parse_int(v)
        return party_to_votes

    @staticmethod
    def loadFromDict(d):
        result = Result(
            d['entity_id'],
            parse_int(d['valid']),
            parse_int(d['rejected']),
            parse_int(d['polled']),
            parse_int(d['electors']),
            Result.extractPartyToVotes(d),
        )
        assert result.valid <= result.polled
        assert result.rejected <= result.polled
        assert result.polled <= result.electors, result
        return result

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
        return Result(
            concat_region_id,
            valid,
            rejected,
            polled,
            electors,
            party_to_votes,
        )
