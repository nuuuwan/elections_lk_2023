import os
from dataclasses import dataclass

from gig import ent_types
from utils.www import read_tsv

from elections_lk.core.ElectionType import ElectionType
from elections_lk.core.Result import Result

GIG2_URL_ROOT = (
    'https://raw.githubusercontent.com/nuuuwan/gig-data/master/gig2'
)


def get_result_idx(raw_result_list, ent_type):
    return dict(
        list(
            map(
                lambda d: [d['entity_id'], Result.loadFromDict(d)],
                list(
                    filter(
                        lambda d: ent_types.get_entity_type(d['entity_id'])
                        == ent_type,
                        raw_result_list,
                    )
                ),
            )
        )
    )


@dataclass
class Election:
    election_type: ElectionType
    year: int
    pd_result_idx: dict
    ed_result_idx: dict
    country_result: Result

    def get_pd_result(self, pd_id):
        return self.pd_result_idx[pd_id]

    def get_ed_result(self, ed_id):
        return self.ed_result_idx[ed_id]

    @staticmethod
    def init(election_type, year):
        raw_result_list = read_tsv(
            os.path.join(
                GIG2_URL_ROOT,
                f'government-elections-{election_type}'
                + f'.regions-ec.{year}.tsv',
            )
        )

        return Election(
            election_type,
            year,
            get_result_idx(raw_result_list, ent_types.ENTITY_TYPE.PD),
            get_result_idx(raw_result_list, ent_types.ENTITY_TYPE.ED),
            get_result_idx(raw_result_list, ent_types.ENTITY_TYPE.COUNTRY)[
                'LK'
            ],
        )
