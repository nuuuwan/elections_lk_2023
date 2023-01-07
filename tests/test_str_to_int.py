from unittest import TestCase

from elections_lk.core.StrToInt import StrToInt

TEST_STR_TO_INT = StrToInt({'a': 1, 'b': 2, 'c': 3})


class TestStrToInt(TestCase):
    def test_init(self):
        s = TEST_STR_TO_INT
        s['d'] = 4
        self.assertEqual(s['a'], 1)
        self.assertEqual(s['b'], 2)
        self.assertEqual(s['c'], 3)
        self.assertEqual(s['d'], 4)
        self.assertEqual(len(s), 4)

    def test_sorted(self):
        s = TEST_STR_TO_INT
        s['d'] = 4
        self.assertEqual(s.items(), [('d', 4), ('c', 3), ('b', 2), ('a', 1)])
