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
