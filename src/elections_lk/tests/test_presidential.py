"""Tests for elections_lk."""

import unittest

from elections_lk import presidential


class TestCase(unittest.TestCase):
    """Tests."""

    def test_get_election_years(self):
        """Test."""
        election_years = presidential.get_election_years()
        self.assertIn(1982, election_years)
        self.assertIn(2019, election_years)

    def test_get_election_data(self):
        """Test."""
        election_data = presidential.get_election_data(2019)
        self.assertGreater(len(election_data), 160)
        first_result = election_data[0]
        self.assertIn('summary', first_result)
        self.assertIn('ed_id', first_result)


if __name__ == '__main__':
    unittest.main()
