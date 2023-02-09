from unittest import TestCase

from elections_lk import ElectionPresidential
from elections_lk.core import SummaryStatistics

TEST_YEAR = 2019
TEST_ELECTION = ElectionPresidential.from_year(TEST_YEAR)


class TestElectionPresidential(TestCase):
    def test_election_type(self):
        election = TEST_ELECTION
        self.assertEqual(election.get_election_type(), 'presidential')

    def test_get_gig_table(self):
        election = TEST_ELECTION
        gig_table = election.get_gig_table(TEST_YEAR)
        self.assertEqual(
            gig_table.measurement, 'government-elections-presidential'
        )
        self.assertEqual(gig_table.ent_type_group, 'regions-ec')
        self.assertEqual(gig_table.time_group, str(TEST_YEAR))

    def test_load(self):
        self.assertEqual(TEST_ELECTION.year, TEST_YEAR)

        pd_results = TEST_ELECTION.pd_results
        self.assertEqual(len(pd_results), 182)
        first_result = pd_results[0]
        self.assertEqual(first_result.region_id, "EC-01A")
        self.assertEqual(first_result.summary_statistics.valid, 72643)
        self.assertEqual(first_result.party_to_votes['SLPP'], 16_986)

    def test_ed_results(self):
        ed_results = TEST_ELECTION.ed_results
        self.assertEqual(len(ed_results), 22)
        first_result = ed_results[0]
        self.assertEqual(first_result.region_id, "EC-01")
        self.assertEqual(first_result.summary_statistics.valid, 1368177)
        self.assertEqual(first_result.party_to_votes['SLPP'], 727_713)

    def test_country_final_results(self):
        country_final_result = TEST_ELECTION.country_final_result

        self.assertEqual(country_final_result.region_id, "LK")
        self.assertEqual(
            country_final_result.summary_statistics.valid, 13_252_499
        )
        self.assertEqual(
            country_final_result.party_to_votes['SLPP'], 6_924_255
        )
        self.assertEqual(country_final_result.total_seats, 1)
        self.assertEqual(country_final_result.party_to_seats['SLPP'], 1)

    def test_2019_election(self):
        election = TEST_ELECTION
        country_final_result = election.country_final_result
        self.assertEqual(country_final_result.region_id, "LK")
        print(country_final_result.summary_statistics)
        self.assertEqual(
            country_final_result.summary_statistics,
            SummaryStatistics(
                valid=13_252_499,
                rejected=135_452,
                polled=13_387_951,
                electors=15_992_568,
            ),
        )
