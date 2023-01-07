from dataclasses import dataclass
from functools import cached_property

from elections_lk.core import FinalResult, Result
from elections_lk.elections.Election import Election


@dataclass
class ElectionPresidential(Election):
    pd_results: list[Result]

    election_type = 'presidential'
    years = [1982, 1988, 1994, 1999, 2005, 2010, 2015, 2019]

    @cached_property
    def ed_results(self) -> list[Result]:
        return Result.mapAndConcat(
            self.pd_results, lambda entity_id: entity_id[:5]
        )

    @cached_property
    def country_final_result(self) -> FinalResult:
        country_result = Result.concat('LK', self.pd_results)
        winning_party = country_result.party_to_votes.keys_sorted()[0]
        return FinalResult.fromResult(
            country_result,
            party_to_seats={winning_party: 1},
        )
