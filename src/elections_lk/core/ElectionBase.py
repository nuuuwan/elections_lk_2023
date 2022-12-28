from dataclasses import dataclass

from elections_lk.core.ElectionType import ElectionType
from elections_lk.core.Result import Result


@dataclass
class ElectionBase:
    election_type: ElectionType
    year: int
    pd_result_idx: dict
    ed_result_idx: dict
    country_result: Result

    def get_pd_result(self, pd_id):
        return self.pd_result_idx[pd_id]

    def get_ed_result(self, ed_id):
        return self.ed_result_idx[ed_id]

    @property
    def total_polled(self):
        return self.country_result.polled

    @property
    def total_valid(self):
        return self.country_result.valid

    @property
    def party_to_seats(self):
        party_to_seats = {}
        for party, seats in self.country_result.party_to_seats.items():
            party_to_seats[party] = seats

        for ed_result in self.ed_result_idx.values():
            for party, seats in ed_result.party_to_seats.items():
                if party not in party_to_seats:
                    party_to_seats[party] = 0
                party_to_seats[party] += seats
        return party_to_seats
