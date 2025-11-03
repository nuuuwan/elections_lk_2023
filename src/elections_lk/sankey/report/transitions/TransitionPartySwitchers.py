from elections_lk.core.Party import Party
from elections_lk.sankey.report.transitions.AbstractTransition import \
    AbstractTransition


class TransitionPartySwitchers(AbstractTransition):
    @property
    def label(self):
        return "Party Switchers"

    @property
    def emoji(self):
        return "🗳️🔄🗳️"

    def is_match(self, party_x, party_y):
        return all(
            [
                party_x != self.NO_VOTE,
                party_y != self.NO_VOTE,
                Party(party_x).color != Party(party_y).color,
            ]
        )

    def get_description(self, election_x, election_y):
        return (
            "People who voted in both elections — "
            f"{election_x.title} and {election_y.title} — "
            "but for different political alignments,"
            + " indicating a change in partisan preference."
        )

    def get_flow_description(
        self, election_x, election_y, party_x, party_y, votes
    ):
        return (
            f"{votes:,} voters who voted for {party_x} in {election_x.title}"
            + f" voted for {party_y} in {election_y.title}. "
        )
