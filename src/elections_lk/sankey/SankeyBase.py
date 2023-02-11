from functools import cached_property


class SankeyBase:
    def __init__(self, election_x, election_y):
        self.election_x = election_x
        self.election_y = election_y

    @cached_property
    def elections(self):
        return [self.election_x, self.election_y]

    @property
    def title(self):
        return ' -> '.join([election.title for election in self.elections])

    @property
    def id(self):
        return '.'.join([election.id for election in self.elections])
