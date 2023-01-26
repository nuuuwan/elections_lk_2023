from unittest import TestCase

from elections_lk.elections import ElectionLocalAuthority

TEST_YEAR = 2018
TEST_ELECTION = ElectionLocalAuthority.load(TEST_YEAR)


class TestElectionLocalAuthority(TestCase):
    def test_election_type(self):
        election = TEST_ELECTION
        self.assertEqual(election.get_election_type(), 'local-authority')

    def test_get_gig_table(self):
        election = TEST_ELECTION
        gig_table = election.get_gig_table(TEST_YEAR)
        self.assertEqual(
            gig_table.measurement,
            'government-elections-local-authority-votes',
        )
        self.assertEqual(gig_table.ent_type_group, 'regions-lg')
        self.assertEqual(gig_table.time_group, str(TEST_YEAR))

    def test_lg_results(self):
        self.assertEqual(TEST_ELECTION.year, TEST_YEAR)
        lg_results = TEST_ELECTION.lg_results
        self.assertEqual(len(lg_results), 341)
        first_result = lg_results[0]
        self.assertEqual(first_result.region_id, "LG-11001")
        self.assertEqual(first_result.summary_statistics.valid, 284_980)
        self.assertEqual(first_result.party_to_votes['UNP'], 131_353)

    def test_lg_final_results(self):
        self.assertEqual(TEST_ELECTION.year, TEST_YEAR)
        lg_final_results = TEST_ELECTION.lg_final_results
        self.assertEqual(len(lg_final_results), 341)
        first_result = lg_final_results[0]
        self.assertEqual(first_result.region_id, "LG-11001")
        self.assertEqual(first_result.summary_statistics.valid, 284_980)
        self.assertEqual(first_result.party_to_votes['UNP'], 131_353)
        self.assertEqual(first_result.party_to_seats['UNP'], 60)

    def test_district_final_result(self):
        district_final_results = TEST_ELECTION.district_final_results
        self.assertEqual(len(district_final_results), 25)
        first_result = district_final_results[0]
        self.assertEqual(first_result.region_id, "LK-11")
        self.assertEqual(first_result.total_seats, 572)
        self.assertEqual(first_result.party_to_seats['UNP'], 198)

    def test_country_final_result(self):
        country_final_result = TEST_ELECTION.country_final_result
        self.assertEqual(country_final_result.region_id, "LK")
        self.assertEqual(country_final_result.total_seats, 8736)
        self.assertEqual(country_final_result.party_to_seats['SLPP'], 3436)
