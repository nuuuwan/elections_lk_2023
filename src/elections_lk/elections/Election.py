from dataclasses import dataclass
from functools import cached_property

from utils import Log

from elections_lk.core import PartyToVotes, Result, SummaryStatistics

log = Log('Election')


def correct_int(x):
    return (int)(round(x, 0))


@dataclass
class Election:
    year: int
    results: list

    @cached_property
    def all_parties(self):
        return sorted(self.country_final_result.party_to_votes.keys())

    def get_popular_parties(self, p_limit=0.005):
        party_to_votes = self.country_final_result.party_to_votes
        total = party_to_votes.total
        vote_limit = total * p_limit
        return [x[0] for x in party_to_votes.items() if x[1] > vote_limit]

    @classmethod
    def extract_party_to_votes(cls, result_raw):
        party_to_votes = {}
        for k, v in result_raw.dict.items():
            if k not in SummaryStatistics.FIELDS:
                party_to_votes[k] = correct_int(v)
        return PartyToVotes(party_to_votes)

    @classmethod
    def extract_summary_statistics(cls, result_raw):
        return SummaryStatistics(
            valid=correct_int(result_raw.valid),
            rejected=correct_int(result_raw.rejected),
            polled=correct_int(result_raw.polled),
            electors=correct_int(result_raw.electors),
        )

    @classmethod
    def load_result(cls, gig_table, ent):
        try:
            result_raw = ent.gig(gig_table)
        except BaseException:
            return None

        return Result(
            region_id=ent.id,
            summary_statistics=cls.extract_summary_statistics(result_raw),
            party_to_votes=cls.extract_party_to_votes(result_raw),
        )

    @classmethod
    def from_year(cls, year):
        ent_list = cls.get_ent_list()
        gig_table = cls.get_gig_table(year)
        results = []
        for ent in ent_list:
            result = cls.load_result(gig_table, ent)
            if result:
                results.append(result)
        return cls(year=year, results=results)
