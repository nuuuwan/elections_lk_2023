import os

from utils import File, Log, TSVFile

log = Log("PartyContinuity")


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

    def get_lines_for_transition_subset(self, title, transition_subset):
        total_votes = sum(votes for _, _, votes in transition_subset)
        lines = [f"## {title} ({total_votes:,})", ""]
        for party_x, party_y, votes in transition_subset:
            if votes == 0:
                continue
            p_votes = votes / total_votes
            lines.append(
                f"- {party_x} -> {party_y}: {votes:,} ({p_votes:.2%})"
            )
        lines.append("")
        return lines

    def save_md(self):
        transitions = self.sorted_transitions
        election_x = self.election_x
        election_y = self.election_y
        lines = [f"# {election_x.title} -> {election_y.title}", ""]

        lines.extend(
            self.get_lines_for_transition_subset(
                "All Transitions",
                transitions,
            )
        )

        lines.extend(
            self.get_lines_for_transition_subset(
                "New Voters & Abstentions who Voted",
                [
                    (party_x, party_y, votes)
                    for party_x, party_y, votes in transitions
                    if party_x == "no vote" and party_y != "no vote"
                ],
            )
        )

        File(self.transition_report_file_path).write_lines(lines)
        log.info(f"Wrote {self.transition_report_file_path}")
