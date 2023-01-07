from dataclasses import dataclass
from functools import cached_property

from elections_lk.core.EntityID import EntityID
from elections_lk.core.PartyToSeats import PartyToSeats
from elections_lk.core.Result import Result


@dataclass
class FinalResult(Result):
    party_to_seats: PartyToSeats

    @cached_property
    def total_seats(self) -> int:
        return sum(self.party_to_seats.values())

    @staticmethod
    def fromResult(result: Result, party_to_seats: PartyToSeats):
        return FinalResult(
            result.entity_id,
            result.summary_statistics,
            result.party_to_votes,
            party_to_seats,
        )

    @classmethod
    def concat(cls, concat_entity_id: EntityID, result_list: list):

        result = Result.concat(concat_entity_id, result_list)
        party_to_seats = PartyToSeats.concat(
            [r.party_to_seats for r in result_list]
        )

        return FinalResult(
            result.entity_id,
            result.summary_statistics,
            result.party_to_votes,
            party_to_seats,
        )
