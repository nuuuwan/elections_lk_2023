from dataclasses import dataclass
from functools import cached_property

from elections_lk.core.Election import Election
from elections_lk.core.FinalResult import FinalResult
from elections_lk.core.Result import Result
from elections_lk.core.Seats import Seats
from elections_lk.core.StrToInt import StrToInt
from elections_lk.core.YEAR_TO_REGION_TO_SEATS import YEAR_TO_REGION_TO_SEATS

P_LIMIT_ED = 0.05
BONUS_ED = 1

SEATS_NATIONAL_LIST = 29
P_LIMIT_NATIONAL_LIST = 0.0
BONUS_NATIONAL_LIST = 0


def get_ed_final_results(year: int, ed_result: Result) -> FinalResult:
    seats = YEAR_TO_REGION_TO_SEATS[year][ed_result.region_id]
    party_to_seats = StrToInt(
        Seats.get_party_to_seats(
            ed_result.party_to_votes.d,
            seats,
            p_limit=P_LIMIT_ED,
            bonus=BONUS_ED,
        )
    )
    return FinalResult.fromResult(ed_result, seats, party_to_seats)


@dataclass
class ElectionParliamentary(Election):
    pd_results: list[Result]

    election_type = 'parliamentary'

    @cached_property
    def ed_final_results(self) -> list[FinalResult]:
        ed_results = Result.mapAndConcat(
            self.pd_results, lambda region_id: region_id[:5]
        )

        return list(
            map(
                lambda ed_result: get_ed_final_results(self.year, ed_result),
                ed_results,
            )
        )

    @cached_property
    def national_list_final_result(self) -> FinalResult:
        country_result = Result.concat('LK', self.pd_results)
        seats = SEATS_NATIONAL_LIST
        party_to_seats = StrToInt(
            Seats.get_party_to_seats(
                country_result.party_to_votes.d,
                seats,
                p_limit=P_LIMIT_NATIONAL_LIST,
                bonus=BONUS_NATIONAL_LIST,
            )
        )
        return FinalResult.fromResult(country_result, seats, party_to_seats)

    @cached_property
    def country_final_result(self) -> FinalResult:
        raise NotImplementedError