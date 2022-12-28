import os
from dataclasses import dataclass

from utils.www import read_tsv

from elections_lk.core.ElectionType import ElectionType
from elections_lk.core.Result import Result

GIG2_URL_ROOT = (
    'https://raw.githubusercontent.com/nuuuwan/gig-data/master/gig2'
)


def is_pd(d):
    region_id = d['entity_id']
    return len(region_id) == 6 and region_id[:3] == 'EC-'


@dataclass
class Election:
    election_type: ElectionType
    year: int
    pd_result_idx: dict

    def get_pd_result(self, pd_id):
        return self.pd_result_idx[pd_id]

    @staticmethod
    def init(election_type, year):
        raw_result_list = read_tsv(
            os.path.join(
                GIG2_URL_ROOT,
                f'government-elections-{election_type}'
                + f'.regions-ec.{year}.tsv',
            )
        )
        raw_pd_result_list = list(
            filter(
                is_pd,
                raw_result_list,
            )
        )
        pd_result_idx = dict(
            [
                [d['entity_id'], Result.loadFromDict(d)]
                for d in raw_pd_result_list
            ]
        )

        return Election(
            election_type,
            year,
            pd_result_idx,
        )
