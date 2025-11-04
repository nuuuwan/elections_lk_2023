from utils import File, Log

from elections_lk.sankey.report.SankeyReportTransitionReportElectionMixin import \
    SankeyReportTransitionReportElectionMixin
from elections_lk.sankey.report.SankeyReportTransitionReportTransitionMixin import \
    SankeyReportTransitionReportTransitionMixin

log = Log("SankeyReportTransitionReportMixin")


class SankeyReportTransitionReportMixin(
    SankeyReportTransitionReportElectionMixin,
    SankeyReportTransitionReportTransitionMixin,
):

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
            "## Labels",
            "",
            "- **no vote**: Individuals who did not vote in that election"
            + " (includes new, former, or disengaged voters).",
            "- **others**:"
            + " Political parties receiving"
            + f" less than {self.P_OTHER_LIMIT:.1%} of valid votes"
            + " in either election, nationwide.",
            "",
        ]
        lines.extend(self.get_lines_for_executive_summary(transitions))
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
        for before, after in [
            ["no vote", "Non-Voting"],
            [
                "others",
                "Small-Parties",
            ],
        ]:
            content = content.replace(before, after)
        File(self.transition_report_file_path).write(content)
        log.info(f"Wrote {self.transition_report_file_path}")
