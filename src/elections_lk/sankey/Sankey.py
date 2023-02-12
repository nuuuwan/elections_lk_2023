from utils import Log

# ElectionParliamentary, ElectionPresidential
from elections_lk import ElectionParliamentary, ElectionPresidential
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDraw import SankeyDraw
from elections_lk.sankey.SankeyModel import SankeyModel
from elections_lk.sankey.SankeyModelNormalize import SankeyModelNormalize
from elections_lk.sankey.SankeyReport import SankeyReport

log = Log('PartyContinuity')


class Sankey(
    SankeyBase, SankeyModel, SankeyModelNormalize, SankeyReport, SankeyDraw
):
    pass


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
        # ElectionParliamentary.from_year(2004),
        ElectionPresidential.from_year(2005),
        # 2010s
        # ElectionPresidential.from_year(2010),
        # ElectionParliamentary.from_year(2010),
        ElectionPresidential.from_year(2015),
        # ElectionParliamentary.from_year(2015),
        # ElectionLocalAuthority.from_year(2018),
        # ElectionPresidential.from_year(2019),
        # 2020s
        # ElectionParliamentary.from_year(2020),
    ]

    s = Sankey([election_x, election_y], '2005 and 2015 Sri Lankan Presidential Elections')
    s.save()
    s.draw()
