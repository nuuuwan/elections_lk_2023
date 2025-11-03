import os

from utils import Log, TSVFile

log = Log("PartyContinuity")


class SankeyReportMixin:
    @property
    def d_list(self):
        matrix = self.matrix
        d_list = []
        for party_x in matrix:
            d = {"party": party_x}
            for party_y, value in matrix[party_x].items():
                d[party_y] = (
                    round(value, 0) if value > 10 else round(value, 3)
                )
            d_list.append(d)
        return d_list

    @property
    def report_file_path(self):
        return os.path.join(
            "/tmp",
            f"report_{self.election_x.year}_{self.election_y.year}.tsv",
        )

    def save(self):
        TSVFile(self.report_file_path).write(self.d_list)
        log.info(f"Saved {self.report_file_path}")
