from utils import File, Log

from elections_lk.base.ValueDict import ValueDict
from elections_lk.core.Party import Party

log = Log("SankeyReportTransitionReportMixin")


class SankeyReportTransitionReportMixin:

    @property
    def transition_report_file_path(self):
        return self.file_base + ".transition_report.md"

    @property
    def sorted_transitions(self):
        transitions = []
        for party_x, party_y_vector in self.matrix.items():
            for party_y, votes in party_y_vector.items():
                votes_r = int(round(votes, 0))
                transitions.append((party_x, party_y, votes_r))
        transitions.sort(key=lambda x: x[2], reverse=True)
        return transitions

    SUBSET_CONFIG_LIST = [
        [
            "Loyal Voters",
            lambda party_x, party_y: all(
                [
                    party_x != "no vote",
                    party_y != "no vote",
                    Party(party_x).color == Party(party_y).color,
                ]
            ),
            lambda title_x, title_y: f"People who voted in both the {title_x}"
            + f" and the {title_y} for the same party,"
            + " maintaining consistent partisan loyalty.",
        ],
        [
            "Party Switchers",
            lambda party_x, party_y: all(
                [
                    party_x != "no vote",
                    party_y != "no vote",
                    Party(party_x).color != Party(party_y).color,
                ]
            ),
            lambda title_x, title_y: f"People who voted in both the {title_x}"
            + f" and the {title_y} but for different parties,"
            + " showing a change in partisan preference.",
        ],
        [
            "New/Re-engaged Voters",
            lambda party_x, party_y: party_x == "no vote"
            and party_y != "no vote",
            lambda title_x, title_y: f"People who didn't vote in the {title_x}"
            + f" but voted in the {title_y},"
            + " reflecting renewed engagement or new voters.",
        ],
        [
            "Disengaged/Former Voters",
            lambda party_x, party_y: party_x != "no vote"
            and party_y == "no vote",
            lambda title_x, title_y: f"People who voted in the {title_x}"
            + f" but didn't vote in the {title_y},"
            + " indicating withdrawal from participation.",
        ],
        [
            "Non-Voters",
            lambda party_x, party_y: party_x == "no vote"
            and party_y == "no vote",
            lambda title_x, title_y: "People who voted in"
            + f" neither {title_x} nor {title_y}.",
        ],
    ]

    @staticmethod
    def get_lines_for_transition_subset(
        title,
        description,
        transition_subset,
        election_x,
        election_y,
    ):
        total_votes = sum(votes for _, _, votes in transition_subset)
        lines = [f"### {title}", ""]
        if description:
            lines.extend([description, ""])
        lines.append(
            SankeyReportTransitionReportMixin.md_table_row(
                election_x.title, election_y.title, "Votes"
            )
        )
        lines.append(
            SankeyReportTransitionReportMixin.md_table_row(":--", ":--", "--:")
        )
        for party_x, party_y, votes in transition_subset:
            lines.append(
                SankeyReportTransitionReportMixin.md_table_row(
                    party_x, party_y, f"{votes:,}"
                )
            )
        lines.append(
            SankeyReportTransitionReportMixin.md_table_row(
                "**Total Votes**", "", f"**{total_votes:,}**"
            )
        )
        lines.append("")
        return lines

    @staticmethod
    def md_table_row(*values) -> str:
        assert isinstance(values, tuple) and len(values) >= 1
        return "| " + " | ".join([str(v).strip() for v in values]) + " |"

    def get_lines_for_elections_summary(self, election_x, election_y):
        def md_table_row_for_value(label, value_func):
            return SankeyReportTransitionReportMixin.md_table_row(
                f"**{label}**",
                value_func(election_x.country_final_result.summary_statistics),
                value_func(election_y.country_final_result.summary_statistics),
            )

        lines = [
            "## Elections Summary",
            "",
            self.md_table_row("  ", election_x.title, election_y.title),
            self.md_table_row(":--", "--:", "--:"),
            md_table_row_for_value(
                "Registered Voters",
                lambda ss: f"{ss.electors:,}",  # noqa: E501
            ),
            md_table_row_for_value(
                "Turnout",
                lambda ss: f"{ss.p_turnout:.0%}",  # noqa: E501
            ),
            md_table_row_for_value(
                "Rejected",
                lambda ss: f"{ss.p_rejected:.1%}",  # noqa: E501
            ),
            md_table_row_for_value(
                "Valid Votes",
                lambda ss: f"{ss.valid:,}",  # noqa: E501
            ),
            "",
        ]
        return lines

    def get_lines_for_vote_transitions_summary(
        self, transitions, title_x, title_y
    ):
        lines = [
            "## Vote Transitions Summary",
            "",
            SankeyReportTransitionReportMixin.md_table_row(
                "Transition Type", "Total Votes", "Description"
            ),
            SankeyReportTransitionReportMixin.md_table_row(
                ":--", "--:", ":--"
            ),
        ]

        for subset_config in self.SUBSET_CONFIG_LIST:
            title, filter_func, description_func = subset_config
            transition_subset = [
                (party_x, party_y, votes)
                for party_x, party_y, votes in transitions
                if filter_func(party_x, party_y)
            ]
            description = description_func(title_x, title_y)
            total_votes = sum(votes for _, _, votes in transition_subset)
            lines.append(
                SankeyReportTransitionReportMixin.md_table_row(
                    title,
                    f"{total_votes:,}",
                    description,
                )
            )
        total_total_votes = sum(votes for _, _, votes in transitions)
        lines.append(
            SankeyReportTransitionReportMixin.md_table_row(
                "**Final Registered Votes**",
                f"**{total_total_votes:,}**",
                "",
            )
        )
        lines.append("")
        return lines

    @staticmethod
    def get_lines_for_transition_subsets(
        transitions, title_x, title_y, election_x, election_y
    ):
        lines = []
        title_x = f"From **{election_x.title}**"
        title_y = f"To **{election_y.title}**"
        for (
            subset_config
        ) in SankeyReportTransitionReportMixin.SUBSET_CONFIG_LIST:
            title, filter_func, description_func = subset_config
            transition_subset = [
                (party_x, party_y, votes)
                for party_x, party_y, votes in transitions
                if filter_func(party_x, party_y)
            ]
            description = description_func(title_x, title_y)
            lines.extend(
                SankeyReportTransitionReportMixin.get_lines_for_transition_subset(  # noqa: E501
                    title,
                    description,
                    transition_subset,
                    election_x,
                    election_y,
                )
            )
        return lines

    def get_lines(self):
        transitions = self.sorted_transitions
        title_x = f"**{self.election_x.title} Election**"
        title_y = f"**{self.election_y.title} Election**"
        lines = [
            f"# {title_x} -> {title_y}",
            "",
            "An analysis of vote transisions between"
            + f" the {title_x}"
            + f" and the {title_y}",
            "",
            "- **no vote**: Individuals who did not vote in that election"
            + " (includes new, former, or disengaged voters).",
            "- **others**:"
            + " Political parties receiving"
            + f" less than {ValueDict.P_OTHERS:.1%} of valid votes"
            + " in either election.",
            "",
        ]

        lines.extend(
            self.get_lines_for_elections_summary(
                self.election_x, self.election_y
            )
        )
        lines.extend(
            self.get_lines_for_vote_transitions_summary(
                transitions, title_x, title_y
            )
        )
        lines.extend(
            self.get_lines_for_transition_subsets(
                transitions,
                title_x,
                title_y,
                self.election_x,
                self.election_y,
            )
        )

        return lines

    def save_md(self):
        lines = self.get_lines()
        content = "\n".join(lines)
        for before, after in ["no vote", "Non-Voting"], [
            "others",
            "Small-Parties",
        ]:
            content = content.replace(before, after)
        File(self.transition_report_file_path).write(content)
        log.info(f"Wrote {self.transition_report_file_path}")
