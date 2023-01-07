class StrToInt:
    def __init__(self, d: dict[str, int]):
        self.d = d

    def __getitem__(self, key: str) -> int:
        return self.d[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.d[key] = value

    def __delitem__(self, key: str) -> None:
        del self.d[key]

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self):
        return iter(self.d)

    def items(self):
        return sorted(self.d.items(), key=lambda x: x[1], reverse=True)
