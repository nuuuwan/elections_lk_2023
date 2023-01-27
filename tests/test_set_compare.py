from unittest import TestCase

from elections_lk.base import SetCompare

TEST_IDX_A = {
    'a1': {1, 2, 3},
    'a2': {5, 6},
    'a3': {7},
    'a4': {8, 9},
    'a5': {10, 11, 12},
    'a6': {13, 14, 15},
}

TEST_IDX_B = {
    'b1': {1, 2, 3},
    'b2': {5},
    'b3': {6},
    'b4': {7, 8, 9},
    'b5': {10, 11, 13},
    'b6': {12, 14, 15},
}

TEST_COMPARE = SetCompare(TEST_IDX_A, TEST_IDX_B)


class TestSetCompare(TestCase):
    def test_overlaps(self):
        expected_overlaps = {
            'a1': {'b1'},
            'a2': {'b2', 'b3'},
            'a3': {'b4'},
            'a4': {'b4'},
            'a5': {'b5', 'b6'},
            'a6': {'b5', 'b6'},
            'b1': {'a1'},
            'b2': {'a2'},
            'b3': {'a2'},
            'b4': {'a3', 'a4'},
            'b5': {'a5', 'a6'},
            'b6': {'a5', 'a6'},
        }
        self.assertEqual(TEST_COMPARE.overlaps, expected_overlaps)

    def test_compare(self):
        expected_results = dict(
            equal=[
                ({'a1'}, {'b1'}),
                ({'a2'}, {'b2', 'b3'}),
                ({'a3', 'a4'}, {'b4'}),
            ],
            other=[
                ('a5', 'b5'),
                ('a5', 'b6'),
                ('a6', 'b5'),
                ('a6', 'b6'),
            ],
        )

        self.assertEqual(TEST_COMPARE.do(), expected_results)
