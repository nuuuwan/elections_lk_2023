from elections_lk.sankey.report.transitions.AbstractTransition import \
    AbstractTransition


class TransitionDisengagedOrFormerVoters(AbstractTransition):
    @property
    def label(self):
        return "Disengaged or Former Voters"

    @property
    def emoji(self):
        return "🛑"

    def is_match(self, party_x, party_y):
        return (party_x != self.NO_VOTE) and (party_y == self.NO_VOTE)

    def get_description(self, election_x, election_y):
        return (
            f"People who voted in the {election_x.title}"
            + f" but did not vote in the {election_y.title},"
            + " indicating *disengaging from voting or deceasing*."
        )

    def get_flow_description(
        self, election_x, election_y, party_x, party_y, votes
    ):
        return (
            f"{votes:,} people who voted for **{party_x}**"
            + f" in {election_x.title}"
            + f" did not vote in {election_y.title}."
        )
