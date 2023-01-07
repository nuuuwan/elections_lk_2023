from functools import cached_property


class Dict:
    '''Dictionary with some useful methods.'''

    OTHERS = 'Others'

    def __init__(self, d: dict[str, int]):
        self.d = d

    def __getitem__(self, key: str) -> int:
        return self.d.get(key, 0)

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self):
        return iter(self.d)

    def __contains__(self, key: str) -> bool:
        return key in self.d

    def keys(self):
        return self.d.keys()

    def values(self):
        return self.d.values()

    def items(self):
        return self.d.items()

    def items_sorted(self):
        return sorted(self.items(), key=lambda x: x[1], reverse=True)

    def items_othered(self, other_limit=0.1):
        items_othered = {}
        total = self.sum
        v_other_sum = 0
        for k, v in self.items_sorted():
            p = v / total
            if p >= other_limit:
                items_othered[k] = v
            else:
                v_other_sum += v
        items_othered[Dict.OTHERS] = v_other_sum
        return list(items_othered.items())

    def keys_sorted(self):
        return [k for k, v in self.items_sorted()]

    def __eq__(self, other):
        if isinstance(other, Dict):
            return self.d == other.d
        if isinstance(other, dict):
            return self.d == other
        return False

    @cached_property
    def sum(self):
        return sum(self.values())

    @staticmethod
    def concat(d_list):
        d2 = {}
        for d in d_list:
            for k, v in d.items():
                if k not in d2:
                    d2[k] = 0
                d2[k] += v
        return Dict(d2)
