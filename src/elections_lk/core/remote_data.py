import os

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
