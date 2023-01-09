import os
import urllib.parse

from bs4 import BeautifulSoup
from gig import ents
from gig.ent_types import ENTITY_TYPE
from utils import JSONFile

from elections_lk.base import CachedBrowser
from elections_lk.core import (FinalResult, PartyToSeats, PartyToVotes,
                               SummaryStatistics)
from elections_lk.elections import ElectionLocalAuthority

YEAR = 2018

URL_BASE = os.path.join(
    'http://www.adaderana.lk',
    'local-authorities-election-2018',
    'division_result.php?',
)


def parse_int(x):
    x = x.replace(',', '')
    if not x:
        return 0
    return (int)(x)


def get_url(district_name, local_authority_name):
    params = dict(dist_id=district_name, div_id=local_authority_name)
    return URL_BASE + urllib.parse.urlencode(
        params, quote_via=urllib.parse.quote
    )


def get_local_authority_name(ent):
    name = ent['name']
    for before, after in [
        ('MC', 'Municipal Council'),
        ('UC', 'Urban Council'),
        ('PS', 'Pradeshiya Sabha'),
    ]:
        name = name.replace(' ' + before, ' ' + after)
    return name


def parse_lg_result(lg_id, source):
    soup = BeautifulSoup(source, 'html.parser')
    party_to_votes = {}
    party_to_seats = {}
    for div_party_result in soup.find_all(
        'div', class_='dis_ele_result_block'
    ):
        party = (
            div_party_result.find('div', class_='ele_party')
            .find('span')
            .text.strip()
        )
        seats = parse_int(
            div_party_result.find('div', class_='ele_seats')
            .find('span')
            .text.strip()
        )
        votes = parse_int(
            div_party_result.find('div', class_='ele_value')
            .find('span')
            .text.strip()
        )
        party_to_votes[party] = votes
        if seats > 0:
            party_to_seats[party] = seats

    tables = soup.find_all('table')[0]
    vals = []
    for tr in tables.find_all('tr'):
        tds = tr.find_all('td')
        val = parse_int(tds[0].text)
        vals.append(val)
    [valid, rejected, polled, electors] = vals[1:]

    return FinalResult(
        entity_id=lg_id,
        summary_statistics=SummaryStatistics(
            valid, rejected, polled, electors
        ),
        party_to_votes=PartyToVotes(party_to_votes),
        party_to_seats=PartyToSeats(party_to_seats),
    )


def get_election():
    district_ent_idx = ents.get_entity_index(ENTITY_TYPE.DISTRICT)
    lg_ents = ents.get_entities(ENTITY_TYPE.LG)
    browser = CachedBrowser()

    lg_results = []
    for ent in lg_ents:
        lg_id = ent['id']
        print(f'Getting results for {lg_id}')
        local_authority_name = get_local_authority_name(ent)
        district_name = district_ent_idx[ent['district_id']]['name']
        url = get_url(district_name, local_authority_name)
        source = browser.getSource(url)
        lg_result = parse_lg_result(lg_id, source)
        lg_results.append(lg_result)
        break
    browser.quit()
    return ElectionLocalAuthority(YEAR, lg_results)


def main():
    election = get_election()
    JSONFile(
        os.path.join(
            'data',
            f'government-elections-local-authority.regions-lg.{YEAR}.json',
        )
    ).write(election.to_dict())


if __name__ == '__main__':
    main()
