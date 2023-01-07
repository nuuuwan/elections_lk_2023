import os

from gig import ent_types
from utils import timex, www
from utils.cache import cache

from elections_lk.core.Result import Result
from elections_lk.core.SummaryStatistics import SummaryStatistics

GIG2_URL_ROOT = (
    'https://raw.githubusercontent.com/nuuuwan/gig-data/master/gig2'
)
NON_PARTY_FIELDS = ['entity_id', 'valid', 'rejected', 'polled', 'electors']


def parse_int(x):
    try:
        return (int)(round((float)(x), 0))
    except ValueError:
        return 0


@cache('get_raw_result_list', timex.SECONDS_IN.YEAR)
def get_raw_result_list(election_type, year):
    return www.read_tsv(
        os.path.join(
            GIG2_URL_ROOT,
            f'government-elections-{election_type}'
            + f'.regions-ec.{year}.tsv',
        )
    )


def filter_by_entity_type(raw_result_list, entity_type):
    return list(
        filter(
            lambda x: ent_types.get_entity_type(x['entity_id'])
            == entity_type,
            raw_result_list,
        )
    )


def get_result_list(election_type, year, entity_type):
    filtered_raw_result_list = filter_by_entity_type(
        get_raw_result_list(election_type, year), entity_type
    )
    result_list = []
    for raw_result in filtered_raw_result_list:
        party_to_votes = {
            k: parse_int(v)
            for k, v in raw_result.items()
            if k not in NON_PARTY_FIELDS
        }
        result_list.append(
            Result(
                region_id=raw_result['entity_id'],
                summary_statistics=SummaryStatistics(
                    valid=parse_int(raw_result['valid']),
                    rejected=parse_int(raw_result['rejected']),
                    polled=parse_int(raw_result['polled']),
                    electors=parse_int(raw_result['electors']),
                ),
                party_to_votes=party_to_votes,
            )
        )
    result_list = sorted(result_list, key=lambda result: result.region_id)
    return result_list
