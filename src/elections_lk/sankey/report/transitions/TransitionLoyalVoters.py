from elections_lk.core.Party import Party
from elections_lk.sankey.report.transitions.AbstractTransition import \
    AbstractTransition


class TransitionLoyalVoters(AbstractTransition):
    @property
    def label(self):
        return "Loyal Voters"

    def is_match(self, party_x, party_y):
        return all(
            [
                party_x != self.NO_VOTE,
                party_y != self.NO_VOTE,
                Party(party_x).color == Party(party_y).color,
            ]
        )

    def get_description(self, election_x, election_y):
        return (
            "People who voted in both elections — "
            f"{election_x.title} and {election_y.title} — "
            "for the same political alignment,"
            + " maintaining consistent partisan loyalty."
        )
