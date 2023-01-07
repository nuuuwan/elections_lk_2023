from unittest import TestCase

from elections_lk.core.ElectionPresidential import ElectionPresidential

TEST_YEAR = 2019
TEST_ELECTION = ElectionPresidential.load(TEST_YEAR)


class TestElectionPresidential(TestCase):
    def test_load(self):
        self.assertEqual(TEST_ELECTION.year, TEST_YEAR)

        pd_results = TEST_ELECTION.pd_results
        self.assertEqual(len(pd_results), 160)
        first_result = pd_results[0]
        self.assertEqual(first_result.region_id, "EC-01A")
        self.assertEqual(first_result.summary_statistics.valid, 72_643)
        self.assertEqual(first_result.party_to_votes['SLPP'], 16_986)

    def test_ed_results(self):
        ed_results = TEST_ELECTION.ed_results
        self.assertEqual(len(ed_results), 22)
        first_result = ed_results[0]
        self.assertEqual(first_result.region_id, "EC-01")
        self.assertEqual(first_result.summary_statistics.valid, 1_335_215)
        self.assertEqual(first_result.party_to_votes['SLPP'], 705_996)

    def test_country_final_results(self):
        country_final_result = TEST_ELECTION.country_final_result

        self.assertEqual(country_final_result.region_id, "LK")
        self.assertEqual(
            country_final_result.summary_statistics.valid, 12_610_859
        )
        self.assertEqual(
            country_final_result.party_to_votes['SLPP'], 6_548_292
        )
        self.assertEqual(country_final_result.total_seats, 1)
        self.assertEqual(country_final_result.party_to_seats['SLPP'], 1)
