from elections_lk.sankey.report.transitions.AbstractTransition import \
    AbstractTransition


class TransitionConsistentNonVoters(AbstractTransition):
    @property
    def label(self):
        return "Consistent Non-Voters"

    def is_match(self, party_x, party_y):
        return (party_x == self.NO_VOTE) and (party_y == self.NO_VOTE)

    def get_description(self, election_x, election_y):
        return (
            "People who did not vote in either election — "
            f"{election_x.title} or {election_y.title} ."
        )
