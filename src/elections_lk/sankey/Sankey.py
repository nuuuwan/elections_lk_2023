from utils import Log

from elections_lk import ElectionParliamentary
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDraw import SankeyDraw
from elections_lk.sankey.SankeyReport import SankeyReport

log = Log('PartyContinuity')

P_LIMIT = 0.005
NOT_COUNTED = '(Didn\'t Vote or Rejected)'
WIDTH = 1200
HEIGHT = 675


class Sankey(SankeyBase, SankeyReport, SankeyDraw):
    pass


if __name__ == '__main__':
    election_x, election_y = [
        ElectionParliamentary.from_year(2015),
        ElectionParliamentary.from_year(2020),
    ]

    report = Sankey(election_x, election_y)
    report.save()
    report.draw()
