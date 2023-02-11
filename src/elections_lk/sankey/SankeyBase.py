class SankeyBase:
    LABEL_ARROW = '⮕'

    def __init__(self, election_list):
        self.election_list = election_list

    @property
    def election_x(self):
        return self.election_list[0]

    @property
    def election_y(self):
        return self.election_list[1]

    @property
    def title(self):
        return self.LABEL_ARROW.join(
            [election.title for election in self.election_list]
        )

    @property
    def id(self):
        return '.'.join([election.id for election in self.election_list])
