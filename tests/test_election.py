from unittest import TestCase

from elections_lk.elections import Election


class TestElection(TestCase):
    def test_init(self):
        election = Election(2020, [])
        self.assertEqual(election.year, 2020)
