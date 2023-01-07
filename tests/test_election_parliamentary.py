from unittest import TestCase

from elections_lk.core.ElectionParliamentary import ElectionParliamentary

TEST_YEAR = 2020
TEST_ELECTION = ElectionParliamentary.load(TEST_YEAR)


class TestElectionParliamentary(TestCase):
    def test_load(self):
        self.assertEqual(TEST_ELECTION.year, TEST_YEAR)

        pd_results = TEST_ELECTION.pd_results
        self.assertEqual(len(pd_results), 160)
        first_result = pd_results[0]
        self.assertEqual(first_result.region_id, "EC-01A")
        self.assertEqual(first_result.summary_statistics.valid, 63_263)
        self.assertEqual(first_result.party_to_votes['SLPP'], 16_775)

    def test_ed_final_results(self):
        ed_final_results = TEST_ELECTION.ed_final_results
        self.assertEqual(len(ed_final_results), 22)
        first_result = ed_final_results[0]
        self.assertEqual(first_result.region_id, "EC-01")
        self.assertEqual(first_result.seats, 19)
        self.assertEqual(first_result.party_to_seats['SLPP'], 12)

    def test_national_list_final_result(self):
        national_list_final_result = TEST_ELECTION.national_list_final_result
        self.assertEqual(national_list_final_result.region_id, "LK")
        self.assertEqual(national_list_final_result.seats, 29)
        self.assertEqual(
            national_list_final_result.party_to_seats['SLPP'], 17
        )
