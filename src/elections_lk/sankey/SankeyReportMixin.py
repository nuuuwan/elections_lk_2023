import os

from utils import Log

from elections_lk.sankey.SankeyReportMatrixDataMixin import \
    SankeyReportMatrixDataMixin
from elections_lk.sankey.SankeyReportTransitionReportMixin import \
    SankeyReportTransitionReportMixin

log = Log("SankeyReportMixin")


class SankeyReportMixin(
    SankeyReportTransitionReportMixin, SankeyReportMatrixDataMixin
):
    @property
    def d_list(self):
        d_list = []
        for party_x, party_y_vector in self.matrix.items():
            d = {"party": party_x}
            for party_y, votes in party_y_vector.items():
                d[party_y] = (
                    round(votes, 0) if votes > 10 else round(votes, 3)
                )
            d_list.append(d)
        return d_list

    @property
    def file_base(self):
        return os.path.join("/tmp", f"sankey_{self.id}")
