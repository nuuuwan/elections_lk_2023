from unittest import TestCase

from elections_lk.core.Election import Election
from elections_lk.core.ElectionType import ElectionType

TEST_PD_ID = 'EC-01A'
TEST_ED_ID = 'EC-01'
TEST_ELECTION_PRESIDENTIAL = Election.init(ElectionType.PRESIDENTIAL, 2019)
TEST_ELECTION_PARLIAMENTARY = Election.init(ElectionType.PARLIAMENTARY, 2020)


class TestElection(TestCase):
    def test_init_presidential(self):
        election = TEST_ELECTION_PRESIDENTIAL
        self.assertEqual(election.election_type, ElectionType.PRESIDENTIAL)
        self.assertEqual(election.year, 2019)
        self.assertEqual(len(election.pd_result_idx), 160)

        test_pd_result = election.get_pd_result(TEST_PD_ID)
        self.assertEqual(test_pd_result.region_id, TEST_PD_ID)
        self.assertEqual(test_pd_result.valid, 72_642)
        self.assertEqual(
            test_pd_result.seats,
            0,
        )

        test_ed_result = election.get_ed_result(TEST_ED_ID)
        self.assertEqual(test_ed_result.region_id, TEST_ED_ID)
        self.assertEqual(test_ed_result.valid, 1_368_177)
        self.assertEqual(
            test_ed_result.seats,
            0,
        )

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
        self.assertEqual(
            country_result.seats,
            1,
        )

    def test_init_parliamentary(self):
        election = TEST_ELECTION_PARLIAMENTARY
        self.assertEqual(election.election_type, ElectionType.PARLIAMENTARY)
        self.assertEqual(election.year, 2020)
        self.assertEqual(len(election.pd_result_idx), 160)

        test_pd_result = election.get_pd_result(TEST_PD_ID)
        self.assertEqual(test_pd_result.region_id, TEST_PD_ID)
        self.assertEqual(test_pd_result.valid, 63_263)
        self.assertEqual(
            test_pd_result.seats,
            0,
        )

        test_ed_result = election.get_ed_result(TEST_ED_ID)
        self.assertEqual(test_ed_result.region_id, TEST_ED_ID)
        self.assertEqual(test_ed_result.valid, 1_182_775)
        self.assertEqual(
            test_ed_result.seats,
            19,
        )

        country_result = election.country_result
        self.assertEqual(country_result.region_id, 'LK')
        self.assertEqual(country_result.valid, 11_598_936)
        self.assertEqual(country_result.get_party_votes('SLPP'), 6_853_692)
        self.assertEqual(country_result.get_party_votes('SJB'), 2_771_983)
        self.assertEqual(
            country_result.get_party_votes_p('SLPP'), 0.5908897160912001
        )
        self.assertEqual(
            country_result.get_party_votes_p('SJB'), 0.23898597250644368
        )
        self.assertEqual(
            country_result.seats,
            29,
        )
