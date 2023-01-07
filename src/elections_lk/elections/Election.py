from dataclasses import dataclass

from gig import ent_types

from elections_lk.elections import remote_data


@dataclass
class Election:
    '''Base class for all elections.'''

    year: int

    @classmethod
    def load(cls, year: int):
        '''Load election data from remote data source.'''
        result_list = remote_data.get_result_list(
            cls.election_type, year, ent_types.ENTITY_TYPE.PD
        )
        return cls(year, result_list)
