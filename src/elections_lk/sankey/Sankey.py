from functools import cached_property

from utils import Log

# ElectionParliamentary, ElectionPresidential
from elections_lk import ElectionPresidential
from elections_lk.sankey.SankeyDraw import SankeyDraw
from elections_lk.sankey.SankeyModel import SankeyModel
from elections_lk.sankey.SankeyModelNormalize import SankeyModelNormalize
from elections_lk.sankey.SankeyReport import SankeyReport

log = Log('PartyContinuity')


class Sankey(SankeyModel, SankeyModelNormalize, SankeyReport, SankeyDraw):
    @cached_property
    def matrix(self):
        # return self.matrix_optimizer
        return self.matrix_model


if __name__ == '__main__':
    election_x, election_y = [
        # 1980s
        # ElectionPresidential.from_year(1982),
        # ElectionPresidential.from_year(1988),
        # ElectionParliamentary.from_year(1989),
        # 1990s
        # ElectionParliamentary.from_year(1994),
        # ElectionPresidential.from_year(1994),
        # ElectionPresidential.from_year(1999),
        # 2000s
        # ElectionParliamentary.from_year(2000),
        # ElectionParliamentary.from_year(2001),
        # ElectionPresidential.from_year(2004),
        # ElectionParliamentary.from_year(2005),
        # 2010s
        # ElectionPresidential.from_year(2010),
        # ElectionParliamentary.from_year(2010),
        ElectionPresidential.from_year(2015),
        # ElectionParliamentary.from_year(2015),
        # ElectionLocalAuthority.from_year(2018),
        ElectionPresidential.from_year(2019),
        # 2020s
        # ElectionParliamentary.from_year(2020),
    ]

    s = Sankey(election_x, election_y)
    s.save()
    s.draw()
