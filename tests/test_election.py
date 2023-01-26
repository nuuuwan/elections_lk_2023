from unittest import TestCase

from elections_lk.elections import Election

TEST_ELECTION = Election(2020, [])


class ElectionFake(Election):
    pass


TEST_ELECTION_FAKE = ElectionFake(2020, [])


class TestElection(TestCase):
    def test_init(self):
        election = TEST_ELECTION
        self.assertEqual(election.year, 2020)
