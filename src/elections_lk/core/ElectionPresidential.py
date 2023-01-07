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

    @property
    def ed_results(self) -> list[Result]:
        raise NotImplementedError

    @property
    def country_result(self) -> FinalResult:
        raise NotImplementedError

    @classmethod
    def load(cls, year: int) -> Election:
        result_list = remote_data.get_result_list(
            cls.election_type, year, ent_types.ENTITY_TYPE.PD
        )
        return ElectionPresidential(year, result_list)
