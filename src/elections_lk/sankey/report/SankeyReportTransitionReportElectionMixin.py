from elections_lk.base import MarkdownUtils


class SankeyReportTransitionReportElectionMixin:
    def get_lines_for_elections_summary(self):
        def md_table_row_for_value(label, value_func):
            return MarkdownUtils.md_table_row(
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
            MarkdownUtils.md_table_row(
                "  ", self.election_x.title, self.election_y.title
            ),
            MarkdownUtils.md_table_row(":--", "--:", "--:"),
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
