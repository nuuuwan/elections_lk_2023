from unittest import TestCase

from elections_lk.core.StrToInt import StrToInt


class TestStrToInt(TestCase):
    def test_init(self):
        s = StrToInt({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(s['a'], 1)
        self.assertEqual(s['b'], 2)
        self.assertEqual(s['c'], 3)
        self.assertEqual(len(s), 3)

    def test_items_sorted(self):
        s = StrToInt({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(s.items_sorted(), [('c', 3), ('b', 2), ('a', 1)])

    def test_items_othered(self):
        s = StrToInt({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(
            s.items_othered(),
            [('c', 3), ('b', 2), ('a', 1), (StrToInt.OTHERS, 0)],
        )

    def test_keys_sorted(self):
        s = StrToInt({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(s.keys_sorted(), ['c', 'b', 'a'])

    def test_concat(self):
        s1 = StrToInt({'a': 1, 'b': 2, 'c': 3})
        s2 = StrToInt({'a': 12, 'b': 23, 'c': 31})
        self.assertEqual(
            StrToInt.concat([s1, s2]),
            StrToInt({'a': 13, 'b': 25, 'c': 34}),
        )
