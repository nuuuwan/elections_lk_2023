from dataclasses import dataclass

from gig import ent_types

from elections_lk.core import remote_data


@dataclass
class Election:
    year: int

    @classmethod
    def load(cls, year: int):
        result_list = remote_data.get_result_list(
            cls.election_type, year, ent_types.ENTITY_TYPE.PD
        )
        return cls(year, result_list)
