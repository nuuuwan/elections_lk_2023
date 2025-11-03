from elections_lk.sankey.report.transitions.AbstractTransition import \
    AbstractTransition


class TransitionReengagedOrFirstTimeVoters(AbstractTransition):
    @property
    def label(self):
        return "Re-engaged or First-Time Voters"

    def is_match(self, party_x, party_y):
        return (party_x == self.NO_VOTE) and (party_y != self.NO_VOTE)

    def get_description(self, election_x, election_y):
        return (
            f"People who did not vote in the {election_x.title}"
            + f" but voted in the {election_y.title},"
            + " reflecting renewed engagement"
            + " or first-time participation."
        )
