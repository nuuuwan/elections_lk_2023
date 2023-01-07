from dataclasses import dataclass

from elections_lk.core.Result import Result
from elections_lk.core.StrToInt import StrToInt


@dataclass
class FinalResult(Result):
    seats: int
    party_to_seats: StrToInt

    @classmethod
    def concat(cls, concat_region_id, result_list):

        result = Result.concat(concat_region_id, result_list)
        seats = sum([r.seats for r in result_list])
        party_to_seats = {}
        for r in result_list:
            for k, v in r.party_to_seats.items():
                if k not in party_to_seats:
                    party_to_seats[k] = 0
                party_to_seats[k] += v

        return FinalResult(
            result.region_id,
            result.summary_statistics,
            result.party_to_votes,
            seats,
            party_to_seats,
        )
