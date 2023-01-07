from dataclasses import dataclass

from gig import ent_types

from elections_lk.core import remote_data
from elections_lk.core.Election import Election
from elections_lk.core.FinalResult import FinalResult
from elections_lk.core.Result import Result


@dataclass
class ElectionPresidential(Election):
    pd_results: list[Result]

    election_type = 'presidential'

    @classmethod
    def load(cls, year: int) -> Election:
        result_list = remote_data.get_result_list(
            cls.election_type, year, ent_types.ENTITY_TYPE.PD
        )
        return ElectionPresidential(year, result_list)

    @property
    def ed_results(self) -> list[Result]:
        ed_id_to_results = {}
        for result in self.pd_results:
            ed_id = result.region_id[:5]
            if ed_id not in ed_id_to_results:
                ed_id_to_results[ed_id] = []
            ed_id_to_results[ed_id].append(result)

        ed_results = []
        for ed_id, results in ed_id_to_results.items():
            ed_result = Result.concat(ed_id, results)
            ed_results.append(ed_result)
        return ed_results

    @property
    def country_final_result(self) -> FinalResult:
        country_result = Result.concat('LK', self.pd_results)
        winning_party = list(country_result.party_to_votes.items())[0]
        return FinalResult(
            country_result.region_id,
            country_result.summary_statistics,
            country_result.party_to_votes,
            seats=1,
            party_to_seats={winning_party: 1},
        )
