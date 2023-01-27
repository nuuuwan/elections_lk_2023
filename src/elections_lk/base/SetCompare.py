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

    def do(self):
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
