from utils import Hash


class SankeyBase:
    LABEL_ARROW = " ⮕ "

    def __init__(self, election_list, title="Sankey"):
        self.election_list = election_list
        self.title = title

    @property
    def election_x(self):
        return self.election_list[0]

    @property
    def election_y(self):
        return self.election_list[1]

    @property
    def election_end(self):
        return self.election_list[-1]

    @property
    def title_long(self):
        return self.LABEL_ARROW.join(
            [election.short_title for election in self.election_list]
        )

    @property
    def id(self):
        first_election_id = self.election_list[0].id
        last_election_id = self.election_list[-1].id

        all_election_id = "".join(
            [election.id for election in self.election_list]
        )
        h = Hash.md5(all_election_id)[:4]
        return f"{first_election_id}_{last_election_id}_{h}"
