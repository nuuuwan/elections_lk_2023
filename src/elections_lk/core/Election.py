import os

from gig import ent_types
from utils.www import read_tsv

from elections_lk.core.ElectionBase import ElectionBase
from elections_lk.core.ElectionType import ElectionType
from elections_lk.core.Result import Result
from elections_lk.core.YEAR_TO_REGION_TO_SEATS import YEAR_TO_REGION_TO_SEATS

NON_PARTY_FIELDS = ['entity_id', 'valid', 'rejected', 'polled', 'electors']
GIG2_URL_ROOT = (
    'https://raw.githubusercontent.com/nuuuwan/gig-data/master/gig2'
)


def parse_int(x):
    return (int)((float)(x))


def extract_party_to_votes(d):
    party_to_votes = {}
    for k, v in d.items():
        if k not in NON_PARTY_FIELDS:
            party_to_votes[k] = parse_int(v)
    return party_to_votes


def get_result_idx(raw_result_list, ent_type):
    return dict(
        list(
            map(
                lambda d: [
                    d['entity_id'],
                    Result(
                        d['entity_id'],
                        parse_int(d['valid']),
                        parse_int(d['rejected']),
                        parse_int(d['polled']),
                        parse_int(d['electors']),
                        extract_party_to_votes(d),
                        0,
                        {},
                    ),
                ],
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


class Election(ElectionBase):
    def get_seats(self, region_id):
        region_type = ent_types.get_entity_type(region_id)
        if self.election_type == ElectionType.PRESIDENTIAL:
            if region_type == ent_types.ENTITY_TYPE.COUNTRY:
                return 1

        if self.election_type == ElectionType.PARLIAMENTARY:
            if region_type == ent_types.ENTITY_TYPE.COUNTRY:
                return 29
            if region_type == ent_types.ENTITY_TYPE.ED:
                return YEAR_TO_REGION_TO_SEATS[self.year][region_id]

        return 0

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
            get_result_idx(
                raw_result_list,
                ent_types.ENTITY_TYPE.PD,
            ),
            get_result_idx(
                raw_result_list,
                ent_types.ENTITY_TYPE.ED,
            ),
            get_result_idx(
                raw_result_list,
                ent_types.ENTITY_TYPE.COUNTRY,
            )['LK'],
        )
