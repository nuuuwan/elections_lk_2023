import os

from gig import ent_types
from utils import timex, www
from utils.cache import cache

from elections_lk.core import Result, StrToInt, SummaryStatistics

GIG2_URL_ROOT = (
    'https://raw.githubusercontent.com/nuuuwan/gig-data/master/gig2'
)
NON_PARTY_FIELDS = ['entity_id', 'valid', 'rejected', 'polled', 'electors']

CACHE_NAME, CACHE_TIMEOUT = (
    'remote_data-v20230107-1816',
    timex.SECONDS_IN.YEAR,
)


def parse_int(x):
    if not x:
        return 0
    return (int)(round((float)(x), 0))


@cache(CACHE_NAME, CACHE_TIMEOUT)
def get_raw_result_list(election_type, year):
    url = os.path.join(
        GIG2_URL_ROOT,
        f'government-elections-{election_type}' + f'.regions-ec.{year}.tsv',
    )
    return www.read_tsv(url, cached=False)


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
        party_and_str_votes = list(
            filter(
                lambda x: x[0] not in NON_PARTY_FIELDS,
                raw_result.items(),
            )
        )
        party_to_votes = StrToInt(
            dict(
                list(
                    map(
                        lambda x: (x[0], parse_int(x[1])),
                        party_and_str_votes,
                    )
                ),
            )
        )
        result_list.append(
            Result(
                entity_id=raw_result['entity_id'],
                summary_statistics=SummaryStatistics(
                    valid=parse_int(raw_result['valid']),
                    rejected=parse_int(raw_result['rejected']),
                    polled=parse_int(raw_result['polled']),
                    electors=parse_int(raw_result['electors']),
                ),
                party_to_votes=party_to_votes,
            )
        )
    result_list = sorted(result_list, key=lambda result: result.entity_id)
    return result_list
