import os

from gig import ent_types
from utils import timex, www
from utils.cache import cache

from elections_lk.core.ElectionBase import ElectionBase
from elections_lk.core.ElectionType import ElectionType
from elections_lk.core.Result import Result
from elections_lk.core.Seats import Seats
from elections_lk.core.YEAR_TO_REGION_TO_SEATS import YEAR_TO_REGION_TO_SEATS

NON_PARTY_FIELDS = ['entity_id', 'valid', 'rejected', 'polled', 'electors']
GIG2_URL_ROOT = (
    'https://raw.githubusercontent.com/nuuuwan/gig-data/master/gig2'
)


def parse_int(x):
    if not x:
        return 0
    return (int)((float)(x))


def extract_party_to_votes(d):
    party_to_votes = {}
    for k, v in d.items():
        if k not in NON_PARTY_FIELDS:
            party_to_votes[k] = parse_int(v)
    return party_to_votes


def get_seats(election_type, year, region_id):
    region_type = ent_types.get_entity_type(region_id)
    if election_type == ElectionType.PRESIDENTIAL:
        if region_type == ent_types.ENTITY_TYPE.COUNTRY:
            return 1

    if election_type == ElectionType.PARLIAMENTARY:
        if region_type == ent_types.ENTITY_TYPE.COUNTRY:
            return 29
        if region_type == ent_types.ENTITY_TYPE.ED:
            return YEAR_TO_REGION_TO_SEATS[year][region_id]

    return 0


def get_limit_and_bonus(election_type, region_id):
    if election_type == ElectionType.PRESIDENTIAL:
        return [0, 1]
    elif election_type == ElectionType.PARLIAMENTARY:
        region_type = ent_types.get_entity_type(region_id)
        if region_type == ent_types.ENTITY_TYPE.ED:
            return [0.05, 1]
        elif region_type == ent_types.ENTITY_TYPE.COUNTRY:
            return [0, 0]
        elif region_type == ent_types.ENTITY_TYPE.PD:
            return [0, 0]
        else:
            raise Exception('Invalid region type: ' + region_type)
    raise Exception('Invalid election type: ' + election_type)


def get_result(election_type, year, d):
    region_id = d['entity_id']
    party_to_votes = extract_party_to_votes(d)

    seats = get_seats(election_type, year, d['entity_id'])
    limit, bonus = get_limit_and_bonus(election_type, region_id)
    party_to_seats = Seats.get_party_to_seats(
        party_to_votes, seats, limit, bonus
    )

    return Result(
        region_id,
        parse_int(d['valid']),
        parse_int(d['rejected']),
        parse_int(d['polled']),
        parse_int(d['electors']),
        party_to_votes,
        seats,
        party_to_seats,
    )


def filter_by_ent_type(raw_result_list, ent_type):
    return list(
        filter(
            lambda d: ent_types.get_entity_type(d['entity_id']) == ent_type,
            raw_result_list,
        )
    )


def get_result_idx(election_type, year, raw_result_list, ent_type):
    return dict(
        list(
            map(
                lambda d: [
                    d['entity_id'],
                    get_result(election_type, year, d),
                ],
                filter_by_ent_type(raw_result_list, ent_type),
            )
        )
    )


@cache('get_raw_result_list', timex.SECONDS_IN.YEAR)
def get_raw_result_list(election_type, year):
    return www.read_tsv(
        os.path.join(
            GIG2_URL_ROOT,
            f'government-elections-{election_type}'
            + f'.regions-ec.{year}.tsv',
        )
    )


class Election(ElectionBase):
    @staticmethod
    def init(election_type, year):
        raw_result_list = get_raw_result_list(election_type, year)

        return Election(
            election_type,
            year,
            get_result_idx(
                election_type,
                year,
                raw_result_list,
                ent_types.ENTITY_TYPE.PD,
            ),
            get_result_idx(
                election_type,
                year,
                raw_result_list,
                ent_types.ENTITY_TYPE.ED,
            ),
            get_result_idx(
                election_type,
                year,
                raw_result_list,
                ent_types.ENTITY_TYPE.COUNTRY,
            )['LK'],
        )
