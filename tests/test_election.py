from unittest import TestCase

from elections_lk.core.Election import Election
from elections_lk.core.ElectionType import ElectionType

TEST_ELECTION_YEAR = 2019
TEST_PD_ID = 'EC-01A'
TEST_ED_ID = 'EC-01'
TEST_ELECTION = Election.init(ElectionType.PRESIDENTIAL, TEST_ELECTION_YEAR)


class TestElection(TestCase):
    def test_init(self):
        election = TEST_ELECTION
        self.assertEqual(election.election_type, ElectionType.PRESIDENTIAL)
        self.assertEqual(election.year, TEST_ELECTION_YEAR)
        self.assertEqual(len(election.pd_result_idx), 160)

        test_pd_result = election.get_pd_result(TEST_PD_ID)
        self.assertEqual(test_pd_result.region_id, TEST_PD_ID)
        self.assertEqual(test_pd_result.valid, 72_642)

        test_ed_result = election.get_ed_result(TEST_ED_ID)
        self.assertEqual(test_ed_result.region_id, TEST_ED_ID)
        self.assertEqual(test_ed_result.valid, 1_368_177)

        country_result = election.country_result
        self.assertEqual(country_result.region_id, 'LK')
        self.assertEqual(country_result.valid, 13_252_499)
        self.assertEqual(country_result.get_party_votes('SLPP'), 6_924_255)
        self.assertEqual(country_result.get_party_votes('NDF'), 5_564_239)
        self.assertEqual(
            country_result.get_party_votes_p('SLPP'), 0.5224867400480467
        )
        self.assertEqual(
            country_result.get_party_votes_p('NDF'), 0.4198633782202134
        )
