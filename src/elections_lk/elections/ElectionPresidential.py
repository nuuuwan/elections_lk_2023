from functools import cached_property

from elections_lk.core.FinalResult import FinalResult
from elections_lk.core.PartyToSeats import PartyToSeats
from elections_lk.core.Result import Result
from elections_lk.elections.ElectionWithPDResults import ElectionWithPDResults


class ElectionPresidential(ElectionWithPDResults):
    @classmethod
    def get_election_type(cls):
        return "presidential"

    @classmethod
    def get_dates(cls):
        return [
            "1982-10-20",
            "1988-12-19",
            "1994-11-09",
            "1999-12-21",
            "2005-11-17",
            "2010-01-26",
            "2015-01-08",
            "2019-11-16",
            "2024-09-21",
        ]

    @cached_property
    def ed_results(self) -> list[Result]:
        """Get results for each electoral district."""
        return Result.mapAndConcat(
            self.pd_results, lambda region_id: region_id[:5]
        )

    @cached_property
    def country_final_result(self) -> FinalResult:
        """Get final results for the country."""
        country_result = Result.concat("LK", self.pd_results)
        winning_party = country_result.party_to_votes.keys_sorted()[0]
        return FinalResult.fromResult(
            country_result,
            party_to_seats=PartyToSeats({winning_party: 1}),
        )
