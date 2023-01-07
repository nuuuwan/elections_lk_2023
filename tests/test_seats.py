from unittest import TestCase

from elections_lk.core.Seats import Seats


class TestSeats(TestCase):
    def test_get_eligible_party_to_votes(self):
        for party_to_votes, p_limit, expected_qualified_party_set in [
            [dict(UNP=50, SLFP=46, JVP=4), 0.05, dict(UNP=50, SLFP=46)],
            [
                dict(UNP=50, SLFP=46, JVP=4),
                0.01,
                dict(UNP=50, SLFP=46, JVP=4),
            ],
            [
                dict(UNP=50, SLFP=30, JVP=20),
                0.05,
                dict(UNP=50, SLFP=30, JVP=20),
            ],
        ]:
            self.assertEqual(
                expected_qualified_party_set,
                Seats.get_eligible_party_to_votes(party_to_votes, p_limit),
            )

    def test_assign_nonbonus_seats(self):
        for (
            party_to_votes,
            total_seats,
            expected_party_to_non_bonus_seats,
        ) in [
            [dict(UNP=50, SLFP=46, JVP=4), 0, dict()],
            [dict(UNP=50, SLFP=46, JVP=4), 3, dict(UNP=2, SLFP=1)],
            [dict(UNP=50, SLFP=30, JVP=20), 3, dict(UNP=1, SLFP=1, JVP=1)],
            [
                dict(SLPP=674_603, SJB=387_145, NPP=67_600),
                18,
                dict(SLPP=11, SJB=6, NPP=1),
            ],
        ]:
            self.assertEqual(
                expected_party_to_non_bonus_seats,
                Seats.assign_nonbonus_seats(party_to_votes, total_seats),
            )

    def test_get_party_to_seats_ed(self):
        for (party_to_votes, total_seats, expected_party_to_seats,) in [
            [dict(UNP=50, SLFP=46, JVP=4), 0, dict()],
            [dict(UNP=50, SLFP=46, JVP=4), 3, dict(UNP=2, SLFP=1)],
            [dict(UNP=50, SLFP=30, JVP=20), 3, dict(UNP=2, SLFP=1)],
            [
                dict(SLPP=674_603, SJB=387_145, NPP=67_600),
                19,
                dict(SLPP=12, SJB=6, NPP=1),
            ],
        ]:
            self.assertEqual(
                expected_party_to_seats,
                Seats.get_party_to_seats(
                    party_to_votes, total_seats, 0.05, 1
                ),
            )
