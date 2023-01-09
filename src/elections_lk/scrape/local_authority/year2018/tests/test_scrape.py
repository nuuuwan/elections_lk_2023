from unittest import TestCase

from elections_lk.scrape.local_authority.year2018 import scrape


class TestScrape(TestCase):
    def test_get_url(self):
        self.assertEqual(
            scrape.get_url('Colombo', 'Colombo Municipal Council'),
            'http://www.adaderana.lk/local-authorities-election-2018'
            + '/division_result.php?'
            + 'dist_id=Colombo&div_id=Colombo%20Municipal%20Council',
        )
