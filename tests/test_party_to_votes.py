from unittest import TestCase

from elections_lk import PartyToSeats, PartyToVotes

TEST_PARTY_TO_VOTES = PartyToVotes(
    {
        "A": 100,
        "B": 150,
        "C": 250,
    },
)
TEST_PARTY_TO_SEATS_CONFIG = [
    [TEST_PARTY_TO_VOTES, 5, 0.25, 1, PartyToSeats({"B": 2, "C": 3})],
    [
        PartyToVotes(
            {
                "SLPP": 674_603,
                "SJB": 387_145,
                "NPP": 67_600,
                "Others": 53_428,
            }
        ),
        19,
        0.05,
        1,
        PartyToSeats({"SLPP": 12, "SJB": 6, "NPP": 1}),
    ],
]


class TestPartyToVotes(TestCase):
    def test_winning_party(self):
        self.assertEqual(TEST_PARTY_TO_VOTES.winning_party, "C")

    def test_get_eligible_party_to_seats(self):
        self.assertEqual(
            TEST_PARTY_TO_VOTES.get_eligible_party_to_seats(0.25),
            PartyToVotes({"B": 150, "C": 250}),
        )

    def test_get_party_to_bonus_seats(self):
        self.assertEqual(
            TEST_PARTY_TO_VOTES.get_party_to_bonus_seats(1),
            PartyToSeats({"C": 1}),
        )

    def test_get_party_to_int_seats(self):
        self.assertEqual(
            TEST_PARTY_TO_VOTES.get_party_to_int_seats(5),
            PartyToSeats({"A": 1, "B": 1, "C": 2}),
        )

    def test_get_party_to_rem(self):
        self.assertEqual(
            TEST_PARTY_TO_VOTES.get_party_to_rem(5),
            {"A": 0.0, "B": 0.5, "C": 0.5},
        )

    def test_get_party_to_rem_seats(self):
        self.assertEqual(
            PartyToVotes.get_party_to_rem_seats(
                1, {"A": 0.0, "B": 0.5, "C": 0.5}
            ),
            PartyToSeats({"B": 1}),
        )

    def test_party_to_seats(self):
        for (
            party_to_votes,
            total_seats,
            p_limit,
            bonus,
            expected_party_to_seats,
        ) in TEST_PARTY_TO_SEATS_CONFIG:
            self.assertEqual(
                party_to_votes.get_party_to_seats(
                    total_seats, p_limit, bonus
                ),
                expected_party_to_seats,
            )
