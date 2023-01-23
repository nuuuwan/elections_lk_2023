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

    def test_election_type(self):
        election = TEST_ELECTION_FAKE
        self.assertEqual(election.get_election_type(), 'fake')

    def test_get_gig_table(self):
        election = TEST_ELECTION_FAKE
        gig_table = election.get_gig_table(2020)
        self.assertEqual(gig_table.measurement, 'government-elections-fake')
        self.assertEqual(gig_table.ent_type_group, 'regions-ec')
        self.assertEqual(gig_table.time_group, '2020')
