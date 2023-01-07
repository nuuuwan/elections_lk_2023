from dataclasses import dataclass
from functools import cached_property

from elections_lk.core.Result import Result
from elections_lk.core.StrToInt import StrToInt


@dataclass
class FinalResult(Result):
    party_to_seats: StrToInt

    @cached_property
    def seats(self) -> int:
        return sum(self.party_to_seats.values())

    @staticmethod
    def fromResult(result: Result, seats, party_to_seats: StrToInt):
        return FinalResult(
            result.region_id,
            result.summary_statistics,
            result.party_to_votes,
            party_to_seats,
        )

    @classmethod
    def concat(cls, concat_region_id, result_list):

        result = Result.concat(concat_region_id, result_list)
        party_to_seats = StrToInt.concat(
            [r.party_to_seats for r in result_list]
        )

        return FinalResult(
            result.region_id,
            result.summary_statistics,
            result.party_to_votes,
            party_to_seats,
        )
