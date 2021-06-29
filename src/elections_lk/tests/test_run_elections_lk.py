"""Tests for elections_lk."""

import unittest

from elections_lk import run_elections_lk


class TestCase(unittest.TestCase):
    """Tests."""

    def test_run_elections_lk(self):
        """Test."""
        self.assertTrue(run_elections_lk.run_elections_lk())


if __name__ == '__main__':
    unittest.main()
