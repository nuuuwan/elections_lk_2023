import os

from utils import File, Log, TSVFile

from elections_lk.base.ValueDict import ValueDict
from elections_lk.core.Party import Party

log = Log("SankeyReportMixin")


class SankeyReportMixin:
    @property
    def d_list(self):
        d_list = []
        for party_x, party_y_vector in self.matrix.items():
            d = {"party": party_x}
            for party_y, votes in party_y_vector.items():
                d[party_y] = round(votes, 0) if votes > 10 else round(votes, 3)
            d_list.append(d)
        return d_list

    @property
    def file_base(self):
        return os.path.join("/tmp", f"sankey_{self.id}")

    @property
    def matrix_data_file_path(self):
        return self.file_base + ".matrix_data.tsv"

    def save_tsv(self):
        TSVFile(self.matrix_data_file_path).write(self.d_list)
        log.info(f"Wrote {self.matrix_data_file_path}")

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
        self, title, description, transition_subset
    ):
        total_votes = sum(votes for _, _, votes in transition_subset)
        lines = [f"## {title} ({total_votes:,})", ""]
        if description:
            lines.extend([description, ""])
        for party_x, party_y, votes in transition_subset:
            if votes == 0:
                continue
            lines.append(f"- {votes:,} `{party_x}` -> `{party_y}`")
        lines.append("")
        return lines

    def save_md(self):
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
            "- **no vote**: did not vote in that election"
            + " (i.e. new or disengaged voters)",
            "- **others**:"
            + f" parties with less < {ValueDict.P_OTHERS:.1%}"
            + " votes in either election",
            "",
        ]

        lines.extend(
            self.get_lines_for_transition_subset(
                "All Vote Movements",
                "",
                transitions,
            )
        )

        lines.extend(
            self.get_lines_for_transition_subset(
                "Loyal Voters",
                f"People who voted in both the {title_x} and the {title_y}"
                + " for the same party,"
                + " maintaining consistent partisan loyalty.",
                [
                    (party_x, party_y, votes)
                    for party_x, party_y, votes in transitions
                    if party_x != "no vote"
                    and party_y != "no vote"
                    and Party(party_x).color == Party(party_y).color
                ],
            )
        )

        lines.extend(
            self.get_lines_for_transition_subset(
                "Party Switchers",
                f"People who voted in both the {title_x} and the {title_y}"
                + " but for different parties,"
                + " showing a change in partisan preference.",
                [
                    (party_x, party_y, votes)
                    for party_x, party_y, votes in transitions
                    if party_x != "no vote"
                    and party_y != "no vote"
                    and Party(party_x).color != Party(party_y).color
                ],
            )
        )

        lines.extend(
            self.get_lines_for_transition_subset(
                "New/Re-engaged Voters",
                f"People who did not vote in the {title_x}"
                + f" but voted in the {title_y}, reflecting"
                + " renewed engagement or new voters.",
                [
                    (party_x, party_y, votes)
                    for party_x, party_y, votes in transitions
                    if party_x == "no vote" and party_y != "no vote"
                ],
            )
        )

        lines.extend(
            self.get_lines_for_transition_subset(
                "Disengaged Voters",
                "People who voted in the"
                + f" {title_x} but didn't vote in the {title_y},"
                + " indicating withdrawal from participation.",
                [
                    (party_x, party_y, votes)
                    for party_x, party_y, votes in transitions
                    if party_x != "no vote" and party_y == "no vote"
                ],
            )
        )

        lines.extend(
            self.get_lines_for_transition_subset(
                "Non-Voters",
                f"People who voted in neither {title_x} nor {title_y}.",
                [
                    (party_x, party_y, votes)
                    for party_x, party_y, votes in transitions
                    if party_x == "no vote" and party_y == "no vote"
                ],
            )
        )

        content = "\n".join(lines)
        for before, after in ["no vote", "Non-Voting"], [
            "others",
            "Small-Parties",
        ]:
            content = content.replace(before, after)
        File(self.transition_report_file_path).write(content)
        log.info(f"Wrote {self.transition_report_file_path}")
