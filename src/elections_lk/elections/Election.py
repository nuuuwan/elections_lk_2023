from dataclasses import dataclass

from gig import GIGTable
from utils import Log

log = Log('Election')


def correct_int(x):
    return (int)(round(x, 0))


@dataclass
class Election:
    '''Base class for all elections.'''

    year: int

    @classmethod
    def get_election_type(cls):
        return cls.__name__.replace('Election', '').lower()

    @classmethod
    def get_gig_table(cls, year: int):
        measurement = f'government-elections-{cls.get_election_type()}'
        region_str = 'regions-ec'
        time_str = str(year)
        return GIGTable(measurement, region_str, time_str)
