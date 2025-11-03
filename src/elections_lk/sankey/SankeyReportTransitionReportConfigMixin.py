from elections_lk.core.Party import Party


class SankeyReportTransitionReportConfigMixin:
    @staticmethod
    def get_config_list():
        NO_VOTE = "no vote"
        return [
            [
                "Loyal Voters",
                lambda party_x, party_y: all(
                    [
                        party_x != NO_VOTE,
                        party_y != NO_VOTE,
                        Party(party_x).color == Party(party_y).color,
                    ]
                ),
                lambda title_x, title_y: (
                    "People who voted in both elections — "
                    f"{title_x} and {title_y} — "
                    "for the same political alignment,"
                    + " maintaining consistent partisan loyalty."
                ),
            ],
            [
                "Party Switchers",
                lambda party_x, party_y: all(
                    [
                        party_x != NO_VOTE,
                        party_y != NO_VOTE,
                        Party(party_x).color != Party(party_y).color,
                    ]
                ),
                lambda title_x, title_y: (
                    "People who voted in both elections — "
                    f"{title_x} and {title_y} — "
                    "but for different political alignments,"
                    + " indicating a change in partisan preference."
                ),
            ],
            [
                "Re-engaged or First-Time Voters",
                lambda party_x, party_y: (party_x == NO_VOTE)
                and (party_y != NO_VOTE),
                lambda title_x, title_y: (
                    f"People who did not vote in the {title_x}"
                    + f" but voted in the {title_y},"
                    + " reflecting renewed engagement"
                    + " or first-time participation."
                ),
            ],
            [
                "Disengaged Voters",
                lambda party_x, party_y: (party_x != NO_VOTE)
                and (party_y == NO_VOTE),
                lambda title_x, title_y: (
                    f"People who voted in the {title_x}"
                    + f" but did not vote in the {title_y},"
                    + " indicating withdrawal from participation."
                ),
            ],
            [
                "Consistent Non-Voters",
                lambda party_x, party_y: (party_x == NO_VOTE)
                and (party_y == NO_VOTE),
                lambda title_x, title_y: (
                    "People who did not vote in either election — "
                    f"{title_x} or {title_y} ."
                ),
            ],
        ]
