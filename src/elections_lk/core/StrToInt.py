class StrToInt:
    def __init__(self, d: dict[str, int]):
        self.d = d

    def __getitem__(self, key: str) -> int:
        return self.d[key]

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

    def keys_sorted(self):
        return [k for k, v in self.items_sorted()]

    def __eq__(self, other):
        if isinstance(other, StrToInt):
            return self.d == other.d
        if isinstance(other, dict):
            return self.d == other
        return False

    @staticmethod
    def concat(str_to_int_list):
        d = {}
        for str_to_int in str_to_int_list:
            for k, v in str_to_int.items():
                if k not in d:
                    d[k] = 0
                d[k] += v
        return StrToInt(d)
