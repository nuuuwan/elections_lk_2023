from unittest import TestCase

from elections_lk.elections.ElectionWithPDResults import ElectionWithPDResults

TEST_ELECTION = ElectionWithPDResults(2020, [])


class TestElectionWithPDResults(TestCase):
    def test_pd_results(self):
        election = TEST_ELECTION
        self.assertEqual(election.pd_results, [])

    def test_get_ent_list(self):
        election = TEST_ELECTION
        self.assertEqual(len(election.get_ent_list()), 183)
