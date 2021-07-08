"""Tests for elections_lk."""

import unittest

from elections_lk import party_color


class TestCase(unittest.TestCase):
    """Tests."""

    def test_party_to_rgb_color(self):
        """Test."""
        for party_id, expected_color in (
            ('UNP', (0, 0.5, 0)),
            ('NDF', (0, 0.5, 0)),
        ):
            self.assertEqual(
                expected_color,
                party_color.get_rgb_color(party_id),
            )

    def test_party_to_rgba_color(self):
        """Test."""
        for party_id, p_votes, expected_color in (
            ('UNP', 0.45, (0, 0.5, 0, 0)),
            ('NDF', 1.0, (0, 0.5, 0, 1)),
        ):
            self.assertEqual(
                expected_color,
                party_color.get_rgba_color(party_id, p_votes),
            )


if __name__ == '__main__':
    unittest.main()
