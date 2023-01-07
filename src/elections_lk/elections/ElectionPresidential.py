from dataclasses import dataclass
from functools import cached_property

from elections_lk.core.FinalResult import FinalResult
from elections_lk.core.Result import Result
from elections_lk.elections.Election import Election


@dataclass
class ElectionPresidential(Election):
    pd_results: list[Result]

    election_type = 'presidential'

    @cached_property
    def ed_results(self) -> list[Result]:
        return Result.mapAndConcat(
            self.pd_results, lambda region_id: region_id[:5]
        )

    @cached_property
    def country_final_result(self) -> FinalResult:
        country_result = Result.concat('LK', self.pd_results)
        winning_party = country_result.party_to_votes.keys_sorted()[0]
        return FinalResult.fromResult(
            country_result,
            party_to_seats={winning_party: 1},
        )
