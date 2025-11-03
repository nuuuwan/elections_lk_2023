from utils import File, Log

from elections_lk.base.ValueDict import ValueDict
from elections_lk.sankey.report.transitions.VoteTransitionFactory import (
    VoteTransitionFactory,
)

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

    def get_lines_for_transition_subset(
        self,
        title,
        description,
        transition_subset,
    ):
        total_votes = sum(votes for _, _, votes in transition_subset)
        lines = [f"### {title}", ""]
        if description:
            lines.extend([description, ""])
        lines.append(
            SankeyReportTransitionReportMixin.md_table_row(
                self.election_x.title, self.election_y.title, "Votes"
            )
        )
        lines.append(
            SankeyReportTransitionReportMixin.md_table_row(":--", ":--", "--:")
        )
        MIN_VOTES = 10_000
        for party_x, party_y, votes in transition_subset:
            if votes < MIN_VOTES:
                continue
            lines.append(
                SankeyReportTransitionReportMixin.md_table_row(
                    party_x, party_y, f"{votes:,}"
                )
            )
        lines.append(
            SankeyReportTransitionReportMixin.md_table_row(
                "**Total Registered Votes**", "", f"**{total_votes:,}**"
            )
        )
        lines.append("")
        return lines

    @staticmethod
    def md_table_row(*values) -> str:
        assert isinstance(values, tuple) and len(values) >= 1
        return "| " + " | ".join([str(v).strip() for v in values]) + " |"

    def get_lines_for_elections_summary(self):
        def md_table_row_for_value(label, value_func):
            return SankeyReportTransitionReportMixin.md_table_row(
                f"**{label}**",
                value_func(
                    self.election_x.country_final_result.summary_statistics
                ),
                value_func(
                    self.election_y.country_final_result.summary_statistics
                ),
            )

        lines = [
            "## Elections Summary",
            "",
            self.md_table_row(
                "  ", self.election_x.title, self.election_y.title
            ),
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
        self,
        transitions,
    ):
        lines = [
            "## Vote Transitions",
            "",
            "### Summary",
            "",
            SankeyReportTransitionReportMixin.md_table_row(
                "Voter Type", "Total Registered Votes", "%", "Description"
            ),
            SankeyReportTransitionReportMixin.md_table_row(
                ":--", "--:", "--:", ":--"
            ),
        ]

        transition_subset_idx = VoteTransitionFactory.split_transitions(
            transitions
        )
        transition_idx = VoteTransitionFactory.get_transition_idx()
        total_total_votes = sum(votes for _, _, votes in transitions)
        for i_subset, (label, transition_subset) in enumerate(
            transition_subset_idx.items(), start=1
        ):
            transition = transition_idx[label]
            description = transition.get_description(
                self.election_x, self.election_y
            )
            total_votes = sum(votes for _, _, votes in transition_subset)
            p_total_votes = total_votes / total_total_votes
            lines.append(
                SankeyReportTransitionReportMixin.md_table_row(
                    f"`Type {i_subset}` {label}",
                    f"{total_votes:,}",
                    f"{p_total_votes:.0%}",
                    description,
                )
            )

        lines.append(
            SankeyReportTransitionReportMixin.md_table_row(
                "**Final Registered Votes**",
                f"**{total_total_votes:,}**",
                "**100%**",
                "",
            )
        )
        lines.append("")
        return lines

    def get_lines_for_transition_subsets(
        self,
        transitions,
    ):
        lines = []
        transition_idx = VoteTransitionFactory.get_transition_idx()
        transition_subset_idx = VoteTransitionFactory.split_transitions(
            transitions
        )
        for i_subset, (label, transition_subset) in enumerate(
            transition_subset_idx.items(), start=1
        ):
            transition = transition_idx[label]
            description = transition.get_description(
                self.election_x, self.election_y
            )
            lines.extend(
                self.get_lines_for_transition_subset(
                    f"`Type {i_subset}` {label}",
                    description,
                    transition_subset,
                )
            )
        return lines

    def get_lines(self):
        transitions = self.sorted_transitions
        image_file_path = self.image_file_path
        lines = [
            f"# {self.election_x.title} -> {self.election_y.title}",
            "",
            "An analysis of vote transitions between"
            + f" the {self.election_x.title} Election"
            + f" and the {self.election_y.title} Election",
            "",
            f"![Image]({image_file_path})",
            "",
            "- **no vote**: Individuals who did not vote in that election"
            + " (includes new, former, or disengaged voters).",
            "- **others**:"
            + " Political parties receiving"
            + f" less than {self.P_OTHER_LIMIT:.1%} of valid votes"
            + " in either election, nationwide.",
            "",
        ]

        lines.extend(self.get_lines_for_elections_summary())
        lines.extend(
            self.get_lines_for_vote_transitions_summary(
                transitions,
            )
        )
        lines.extend(
            self.get_lines_for_transition_subsets(
                transitions,
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
