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
            lambda title_x, title_y: f"People who voted in both the {title_x} and the {title_y} for the same party, maintaining consistent partisan loyalty.",
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
            lambda title_x, title_y: f"People who voted in both the {title_x} and the {title_y} but for different parties, showing a change in partisan preference.",
        ],
        [
            "New/Re-engaged Voters",
            lambda party_x, party_y: party_x == "no vote"
            and party_y != "no vote",
            lambda title_x, title_y: f"People who did not vote in the {title_x} but voted in the {title_y}, reflecting renewed engagement or new voters.",
        ],
        [
            "Disengaged Voters",
            lambda party_x, party_y: party_x != "no vote"
            and party_y == "no vote",
            lambda title_x, title_y: f"People who voted in the {title_x} but didn't vote in the {title_y}, indicating withdrawal from participation.",
        ],
        [
            "Non-Voters",
            lambda party_x, party_y: party_x == "no vote"
            and party_y == "no vote",
            lambda title_x, title_y: f"People who voted in neither {title_x} nor {title_y}.",
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
        lines = [f"## {title} ({total_votes:,})", ""]
        if description:
            lines.extend([description, ""])
        lines.append(
            SankeyReportMixin.md_table_row(
                election_x.title, election_y.title, "Votes"
            )
        )
        lines.append(SankeyReportMixin.md_table_row(":--", ":--", "--:"))
        for party_x, party_y, votes in transition_subset:
            lines.append(
                SankeyReportMixin.md_table_row(party_x, party_y, f"{votes:,}")
            )
        lines.append("")
        return lines

    @staticmethod
    def md_table_row(*values):
        return "| " + " | ".join([str(v).strip() for v in values]) + " |"

    def get_lines_for_elections(self, election_x, election_y):
        def md_table_row_for_value(label, value_func):
            return SankeyReportMixin.md_table_row(
                f"**{label}**",
                value_func(election_x),
                value_func(election_y),
            )

        lines = [
            "## Elections Summary",
            "",
            self.md_table_row("...", election_x.title, election_y.title),
            self.md_table_row(":--", "--:", "--:"),
            md_table_row_for_value(
                "Total Votes",
                lambda e: f"{e.country_final_result.total_votes:,}",
            ),
            md_table_row_for_value(
                "Turnout",
                lambda e: f"{e.country_final_result.summary_statistics.p_turnout:.0%}",  # noqa: E501
            ),
            md_table_row_for_value(
                "Rejected",
                lambda e: f"{e.country_final_result.summary_statistics.p_rejected:.1%}",  # noqa: E501
            ),
            "",
        ]
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
            self.get_lines_for_elections(self.election_x, self.election_y)
        )

        for subset_config in self.SUBSET_CONFIG_LIST:
            title, filter_func, description_func = subset_config
            transition_subset = [
                (party_x, party_y, votes)
                for party_x, party_y, votes in transitions
                if filter_func(party_x, party_y)
            ]
            description = description_func(title_x, title_y)
            lines.extend(
                SankeyReportMixin.get_lines_for_transition_subset(
                    title,
                    description,
                    transition_subset,
                    self.election_x,
                    self.election_y,
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
