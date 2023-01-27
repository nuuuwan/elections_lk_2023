from functools import cached_property


class SetCompare:
    def __init__(self, idx_a: dict[str, set], idx_b: dict[str:set]):
        self.idx_a = idx_a
        self.idx_b = idx_b

    @cached_property
    def overlaps(self):
        overlaps = {}
        for id_a, fp_a in self.idx_a.items():
            for id_b, fp_b in self.idx_b.items():
                if fp_a.intersection(fp_b):
                    if id_a not in overlaps:
                        overlaps[id_a] = set()
                    overlaps[id_a].add(id_b)
                    if id_b not in overlaps:
                        overlaps[id_b] = set()
                    overlaps[id_b].add(id_a)
        return overlaps

    def is_proper_superset(self, id_a):
        overlaps = self.overlaps
        return all([overlaps[id_b] == {id_a} for id_b in overlaps[id_a]])

    @property
    def results(self):
        overlaps = self.overlaps

        # equal
        equal_ids = set()
        equal = []
        # equal-a: 1 to 1, 1 to n
        for id_a in self.idx_a:
            if self.is_proper_superset(id_a):
                equal.append(({id_a}, overlaps[id_a]))
                equal_ids.add(id_a)
                equal_ids.update(overlaps[id_a])

        # equal-b: n to 1 (1 to 1 should not be repeated)
        for id_b in self.idx_b:
            if len(overlaps[id_b]) != 1:
                if self.is_proper_superset(id_b):
                    equal.append((overlaps[id_b], {id_b}))
                    equal_ids.add(id_b)
                    equal_ids.update(overlaps[id_b])

        # other_overlaps
        other = []
        for id_a in self.idx_a:
            if id_a in equal_ids:
                continue
            for id_b in self.idx_b:
                if id_b in equal_ids:
                    continue
                if id_a in overlaps[id_b]:
                    other.append((id_a, id_b))

        return dict(equal=equal, other=other)


if __name__ == '__main__':
    idx_a = {
        'a1': {1, 2, 3},
        'a2': {5, 6},
        'a3': {7},
        'a4': {8, 9},
        'a5': {10, 11, 12},
        'a6': {13, 14, 15},
    }

    idx_b = {
        'b1': {1, 2, 3},
        'b2': {5},
        'b3': {6},
        'b4': {7, 8, 9},
        'b5': {10, 11, 13},
        'b6': {12, 14, 15},
    }

    sc = SetCompare(idx_a, idx_b)

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
    assert sc.overlaps == expected_overlaps

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

    actual_results = sc.results
    assert actual_results == expected_results, actual_results
