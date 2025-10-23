from utils import Log

from elections_lk import ElectionPresidential
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDraw import SankeyDraw
from elections_lk.sankey.SankeyModel import SankeyModel
from elections_lk.sankey.SankeyModelNormalize import SankeyModelNormalize
from elections_lk.sankey.SankeyReport import SankeyReport

log = Log("PartyContinuity")


class Sankey(
    SankeyBase, SankeyModel, SankeyModelNormalize, SankeyReport, SankeyDraw
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
