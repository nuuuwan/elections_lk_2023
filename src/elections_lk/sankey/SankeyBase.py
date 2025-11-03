from utils import Hash


class SankeyBase:
    LABEL_ARROW = " ⮕ "

    def __init__(self, election_x, election_y, title):
        self.election_x = election_x
        self.election_y = election_y
        self.title = title

    @property
    def election_list(self):
        return [self.election_x, self.election_y]

    @property
    def title_long(self):
        return self.LABEL_ARROW.join(
            [election.short_title for election in self.election_list]
        )

    @property
    def id(self):
        id_election_x = self.election_x.id
        id_election_y = self.election_y.id

        all_election_id = "".join(
            [election.id for election in self.election_list]
        )
        h = Hash.md5(all_election_id)[:4]
        return f"{id_election_x}_{id_election_y}_{h}"
