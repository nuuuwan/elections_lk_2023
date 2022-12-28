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
