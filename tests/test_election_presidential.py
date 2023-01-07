from unittest import TestCase

from elections_lk.core.ElectionPresidential import ElectionPresidential


class TestElectionPresidential(TestCase):
    def test_load(self):
        year = 2019
        election = ElectionPresidential.load(year)
        self.assertEqual(election.year, year)
        self.assertEqual(len(election.pd_results), 160)
        first_result = election.pd_results[0]
        self.assertEqual(first_result.region_id, "EC-01A")
        self.assertEqual(first_result.summary_statistics.valid, 72_643)
        self.assertEqual(first_result.party_to_votes['SLPP'], 16_986)
