from dataclasses import dataclass
from functools import cached_property

from elections_lk.base.ValueDict import ValueDict


@dataclass
class ElectionBase:
    date: str
    results: list

    def get_election_type(self):
        raise NotImplementedError

    @property
    def year(self):
        return int(self.date[:4])

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
    def date_id(self):
        return self.date.replace("-", "")

    @property
    def id(self):
        return f"{self.date_id}_{self.get_election_type()}"

    @property
    def results_idx(self):
        return {result.region_id: result for result in self.results}

    @cached_property
    def all_parties(self):
        return sorted(self.country_final_result.party_to_votes.keys())

    def get_popular_parties(self, P_OTHER_LIMIT):
        party_to_votes = self.country_final_result.party_to_votes
        total = party_to_votes.total
        vote_limit = total * P_OTHER_LIMIT
        return [
            x[0]
            for x in sorted(
                party_to_votes.items(), key=lambda x: x[1], reverse=False
            )
            if x[1] > vote_limit
        ] + [ValueDict.OTHERS]

    @classmethod
    def get_dates(cls):
        raise NotImplementedError

    @classmethod
    def get_years(cls):
        years = []
        for date in cls.get_dates():
            year = int(date[:4])
            years.append(year)
        return years

    @classmethod
    def get_ent_list(cls):
        raise NotImplementedError

    @classmethod
    def get_gig_table(cls, __):
        raise NotImplementedError
