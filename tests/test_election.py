from unittest import TestCase

from elections_lk.core.Election import Election
from elections_lk.core.ElectionType import ElectionType

TEST_ELECTION_YEAR = 2019
TEST_PD_ID = 'EC-01A'
TEST_ELECTION = Election.init(ElectionType.PRESIDENTIAL, TEST_ELECTION_YEAR)


class TestElection(TestCase):
    def test_init(self):
        election = TEST_ELECTION
        self.assertEqual(election.election_type, ElectionType.PRESIDENTIAL)
        self.assertEqual(election.year, TEST_ELECTION_YEAR)
        self.assertEqual(len(election.pd_result_idx), 160)

        test_result = election.get_pd_result(TEST_PD_ID)
        self.assertEqual(test_result.region_id, TEST_PD_ID)
