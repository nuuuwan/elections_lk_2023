from elections_lk.sankey.report.transitions.AbstractTransition import \
    AbstractTransition


class TransitionNonVoters(AbstractTransition):
    @property
    def label(self):
        return "Non-Voters"

    @property
    def emoji(self):
        return "🚫"

    def is_match(self, party_x, party_y):
        return (party_x == self.NO_VOTE) and (party_y == self.NO_VOTE)

    def get_description(self, election_x, election_y):
        return (
            "People who did not vote in either election — "
            f"{election_x.title} or {election_y.title} ."
        )

    def get_flow_description(
        self, election_x, election_y, party_x, party_y, votes
    ):
        return (
            f"{votes:,} people did not vote in either of"
            + f" {election_x.title} or {election_y.title}."
        )
