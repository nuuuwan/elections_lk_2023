from dataclasses import dataclass
from functools import cached_property

from gig import GIGTable
from utils import Log

from elections_lk.base.ValueDict import ValueDict
from elections_lk.core.PartyToVotes import PartyToVotes
from elections_lk.core.Result import Result
from elections_lk.core.SummaryStatistics import SummaryStatistics

log = Log("Election")


def correct_int(x):
    return (int)(round(x, 0))


@dataclass
class Election:
    year: int
    results: list

    def get_election_type(self):
        raise NotImplementedError

    @property
    def country_final_result(self):
        raise NotImplementedError

    @property
    def title(self):
        return f"{self.year} {self.get_election_type().title()}"

    @property
    def short_title(self):
        return f"{self.year} {self.get_election_type().title()[:5]}."

    @property
    def id(self):
        return f"{self.get_election_type()[:2]}{self.year}"

    @property
    def results_idx(self):
        return {result.region_id: result for result in self.results}

    @cached_property
    def all_parties(self):
        return sorted(self.country_final_result.party_to_votes.keys())

    def get_popular_parties(self, p_limit=0.005):
        party_to_votes = self.country_final_result.party_to_votes
        total = party_to_votes.total
        vote_limit = total * p_limit
        return [
            x[0]
            for x in sorted(
                party_to_votes.items(), key=lambda x: x[1], reverse=False
            )
            if x[1] > vote_limit
        ] + [ValueDict.OTHERS]

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

        party_to_votes = cls.extract_party_to_votes(result_raw)

        # HACK Fix for 2000 Parliamentary Election missing Summary Statistics
        if (
            gig_table.measurement == "government-elections-parliamentary"
            and gig_table.time_group == "2000"
        ):
            gig_table2 = GIGTable(
                gig_table.measurement, gig_table.ent_type_group, "2001"
            )
            result_raw2 = ent.gig(gig_table2)
            summary_statistics = cls.extract_summary_statistics(result_raw2)
            valid = party_to_votes.total
            summary_statistics.valid = valid
        else:
            summary_statistics = cls.extract_summary_statistics(result_raw)

        return Result(
            region_id=ent.id,
            summary_statistics=summary_statistics,
            party_to_votes=party_to_votes,
        )

    @classmethod
    def get_years(cls):
        raise NotImplementedError

    @classmethod
    def get_ent_list(cls):
        raise NotImplementedError

    @classmethod
    def get_gig_table(cls, __):
        raise NotImplementedError

    @classmethod
    def from_year(cls, year):
        if year not in cls.get_years():
            raise ValueError(f"Invalid year: {year}")

        ent_list = cls.get_ent_list()
        gig_table = cls.get_gig_table(year)
        results = []
        for ent in ent_list:
            result = cls.load_result(gig_table, ent)
            if result:
                results.append(result)
        return cls(year=year, results=results)
