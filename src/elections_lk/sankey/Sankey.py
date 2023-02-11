from functools import cached_property

from utils import Log

# ElectionParliamentary, ElectionPresidential
from elections_lk import ElectionPresidential, ElectionParliamentary
from elections_lk.sankey.SankeyDraw import SankeyDraw
from elections_lk.sankey.SankeyModel import SankeyModel
from elections_lk.sankey.SankeyOptimizer import SankeyOptimizer
from elections_lk.sankey.SankeyReport import SankeyReport

log = Log('PartyContinuity')


class Sankey(SankeyModel, SankeyOptimizer, SankeyReport, SankeyDraw):
    @cached_property
    def matrix(self):
        # return self.matrix_optimizer
        return self.matrix_model


if __name__ == '__main__':
    election_x, election_y = [
        ElectionPresidential.from_year(1994),        
        ElectionPresidential.from_year(1999), 
    ]

    s = Sankey(election_x, election_y)
    s.save()
    s.draw()
