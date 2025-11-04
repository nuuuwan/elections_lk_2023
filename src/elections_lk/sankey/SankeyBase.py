import os

from utils import Hash


class SankeyBase:
    P_OTHER_LIMIT = 0.01
    LABEL_ARROW = " ⮕ "
    DIR_TMP_SANKEY = os.path.join("/tmp", "sankey")

    def __init__(self, election_x, election_y, title, include_others):
        self.election_x = election_x
        self.election_y = election_y
        self.title = title
        self.include_others = include_others

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

    @property
    def file_base(self):
        os.makedirs(self.DIR_TMP_SANKEY, exist_ok=True)
        others_label = (
            "with_others" if self.include_others else "without_others"
        )
        return os.path.join(
            self.DIR_TMP_SANKEY, f"sankey_{self.id}_{others_label}"
        )
