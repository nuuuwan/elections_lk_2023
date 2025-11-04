from elections_lk.base import MarkdownUtils
from elections_lk.sankey.report.transitions.VoteTransitionFactory import \
    VoteTransitionFactory


class SankeyReportTransitionReportTransitionMixin:

    P_EXECUTIVE_SUMMARY_LIMIT = 0.01

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
            MarkdownUtils.md_table_row(
                self.election_x.title, self.election_y.title, "Votes"
            )
        )
        lines.append(MarkdownUtils.md_table_row(":--", ":--", "--:"))
        MIN_VOTES = 10_000
        for party_x, party_y, votes in transition_subset:
            if votes < MIN_VOTES:
                continue
            lines.append(
                MarkdownUtils.md_table_row(party_x, party_y, f"{votes:,}")
            )
        lines.append(
            MarkdownUtils.md_table_row(
                "**Total Registered Votes**", "", f"**{total_votes:,}**"
            )
        )
        lines.append("")
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
            MarkdownUtils.md_table_row(
                "Voter Type", "Total Registered Votes", "%", "Description"
            ),
            MarkdownUtils.md_table_row(":--", "--:", "--:", ":--"),
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
                MarkdownUtils.md_table_row(
                    f"{i_subset}. {label} {transition.emoji}",
                    f"{total_votes:,}",
                    f"{p_total_votes:.0%}",
                    description,
                )
            )

        lines.append(
            MarkdownUtils.md_table_row(
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
                    f"{i_subset}. {label} {transition.emoji}",
                    description,
                    transition_subset,
                )
            )
        return lines

    def get_lines_for_executive_summary(self, transitions):
        lines = ["## Executive Summary", ""]
        total_votes = sum(votes for _, _, votes in transitions)
        for party_x, party_y, votes in transitions:
            p_votes = votes / total_votes
            if p_votes < self.P_EXECUTIVE_SUMMARY_LIMIT:
                continue
            transition = (
                VoteTransitionFactory.get_transition_for_party_transition(
                    party_x, party_y
                )
            )
            flow_description = transition.get_flow_description(
                self.election_x,
                self.election_y,
                party_x,
                party_y,
                votes,
            )
            lines.append(f"- {transition.emoji} {flow_description}")
        lines.append("")
        return lines
