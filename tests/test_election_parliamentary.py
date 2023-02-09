from unittest import TestCase

from elections_lk import ElectionParliamentary
from elections_lk.core import SummaryStatistics

TEST_YEAR = 2020
TEST_ELECTION = ElectionParliamentary.from_year(TEST_YEAR)


class TestElectionParliamentary(TestCase):
    def test_election_type(self):
        election = TEST_ELECTION
        self.assertEqual(election.get_election_type(), 'parliamentary')

    def test_get_gig_table(self):
        election = TEST_ELECTION
        gig_table = election.get_gig_table(TEST_YEAR)
        self.assertEqual(
            gig_table.measurement, 'government-elections-parliamentary'
        )
        self.assertEqual(gig_table.ent_type_group, 'regions-ec')
        self.assertEqual(gig_table.time_group, '2020')

    def test_load(self):
        self.assertEqual(TEST_ELECTION.year, TEST_YEAR)
        pd_results = TEST_ELECTION.pd_results
        self.assertEqual(len(pd_results), 183)
        first_result = pd_results[0]
        self.assertEqual(first_result.region_id, "EC-01A")
        self.assertEqual(first_result.summary_statistics.valid, 63_263)
        self.assertEqual(first_result.party_to_votes['SLPP'], 16_775)

    def test_ed_final_results(self):
        ed_final_results = TEST_ELECTION.ed_final_results
        self.assertEqual(len(ed_final_results), 22)
        first_result = ed_final_results[0]
        self.assertEqual(first_result.region_id, "EC-01")
        self.assertEqual(first_result.total_seats, 19)
        self.assertEqual(first_result.party_to_seats['SLPP'], 12)

    def test_national_list_final_result(self):
        national_list_final_result = TEST_ELECTION.national_list_final_result
        self.assertEqual(national_list_final_result.region_id, "LK")
        self.assertEqual(national_list_final_result.total_seats, 29)
        self.assertEqual(
            national_list_final_result.party_to_seats['SLPP'], 17
        )

    def test_country_final_result(self):
        country_final_result = TEST_ELECTION.country_final_result
        self.assertEqual(country_final_result.region_id, "LK")
        self.assertEqual(country_final_result.total_seats, 225)
        self.assertEqual(country_final_result.party_to_seats['SLPP'], 145)

    def test_2020_election(self):
        election = TEST_ELECTION
        country_final_result = election.country_final_result
        self.assertEqual(country_final_result.region_id, "LK")
        self.assertEqual(
            country_final_result.summary_statistics,
            SummaryStatistics(
                valid=11_598_936,
                rejected=744_373,
                polled=12_343_309,
                electors=16_544_628,
            ),
        )
