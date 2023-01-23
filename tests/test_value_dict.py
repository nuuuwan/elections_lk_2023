from unittest import TestCase

from elections_lk.base import ValueDict


class TestValueDict(TestCase):
    def test_init(self):
        s = ValueDict({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(s['a'], 1)
        self.assertEqual(s['b'], 2)
        self.assertEqual(s['c'], 3)
        self.assertEqual(len(s), 3)

    def test_items_sorted(self):
        s = ValueDict({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(s.items_sorted(), [('c', 3), ('b', 2), ('a', 1)])

    def test_items_othered(self):
        s = ValueDict({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(
            s.items_othered(),
            [('c', 3), ('b', 2), ('a', 1), (ValueDict.OTHERS, 0)],
        )

    def test_keys_sorted(self):
        s = ValueDict({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(s.keys_sorted(), ['c', 'b', 'a'])

    def test_concat(self):
        s1 = ValueDict({'a': 1, 'b': 2, 'c': 3})
        s2 = ValueDict({'a': 12, 'b': 23, 'c': 31})
        self.assertEqual(
            ValueDict.concat([s1, s2]),
            ValueDict({'a': 13, 'b': 25, 'c': 34}),
        )
