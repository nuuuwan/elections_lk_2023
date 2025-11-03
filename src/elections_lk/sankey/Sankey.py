from utils import Log

from elections_lk import ElectionPresidential
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDrawMixin import SankeyDrawMixin
from elections_lk.sankey.SankeyModelMixin import SankeyModelMixin
from elections_lk.sankey.SankeyModelNormalizeMixin import \
    SankeyModelNormalizeMixin
from elections_lk.sankey.SankeyReportMixin import SankeyReportMixin

log = Log("PartyContinuity")


class Sankey(
    SankeyBase,
    SankeyModelMixin,
    SankeyModelNormalizeMixin,
    SankeyReportMixin,
    SankeyDrawMixin,
):
    pass


if __name__ == "__main__":
    for election_list, title in [
        [
            [
                ElectionPresidential.from_year(2005),
                ElectionPresidential.from_year(2015),
            ],
            "2005 and 2015 Sri Lankan Presidential Elections",
        ],
    ]:

        s = Sankey(election_list, title)
        s.save()
        s.draw()
