from dataclasses import dataclass


def correct_int(x):
    return (int)(round(x, 0))


@dataclass
class Election:
    '''Base class for all elections.'''

    year: int
    pd_results: list

    @classmethod
    def get_election_type(cls):
        return cls.__name__.replace('Election', '').lower()
