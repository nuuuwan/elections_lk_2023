import os

from gig import ent_types
from utils import timex, www
from utils.cache import cache

GIG2_URL_ROOT = (
    'https://raw.githubusercontent.com/nuuuwan/gig-data/master/gig2'
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


def filter_by_entity_type(raw_result_list, entity_type):
    return list(
        filter(
            lambda x: ent_types.get_entity_type(x['entity_id'])
            == entity_type,
            raw_result_list,
        )
    )
