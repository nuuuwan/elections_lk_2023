from dataclasses import dataclass

from elections_lk.core.StrToInt import StrToInt
from elections_lk.core.SummaryStatistics import SummaryStatistics


@dataclass
class Result:
    region_id: str
    summary_statistics: SummaryStatistics
    party_to_votes: StrToInt

    @property
    def valid_long(self):
        return sum(self.party_to_votes.values())

    def get_party_votes(self, party):
        return self.party_to_votes[party]

    def get_party_votes_p(self, party):
        return self.get_party_votes(party) / self.summary_statistics.valid

    @classmethod
    def concat(cls, concat_region_id, result_list):
        summary_statistics = SummaryStatistics.concat(
            [r.summary_statistics for r in result_list]
        )

        party_to_votes = {}
        for r in result_list:
            for k, v in r.party_to_votes.items():
                if k not in party_to_votes:
                    party_to_votes[k] = 0
                party_to_votes[k] += v

        return cls(
            region_id=concat_region_id,
            summary_statistics=summary_statistics,
            party_to_votes=party_to_votes,
        )
