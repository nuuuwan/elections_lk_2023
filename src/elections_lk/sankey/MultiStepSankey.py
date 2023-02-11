from functools import cached_property

from utils import Log

# ElectionParliamentary, ElectionPresidential, ElectionLocalAuthority
from elections_lk import ElectionParliamentary, ElectionPresidential, ElectionLocalAuthority
from elections_lk.sankey.Sankey import Sankey
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDraw import SankeyDraw

log = Log('MultiStepSankey')


class MultiStepSankey(SankeyDraw, SankeyBase):
    @cached_property
    def matrices(self):
        matrices = []
        for election_x, election_y in zip(
            self.election_list[:-1], self.election_list[1:]
        ):
            sankey = Sankey([election_x, election_y])
            matrices.append(sankey.matrix)
        return matrices


if __name__ == '__main__':
    for election_list, title in [
        [
            [
                ElectionParliamentary.from_year(1989),
                ElectionParliamentary.from_year(1994),
                ElectionParliamentary.from_year(2000),
                ElectionParliamentary.from_year(2001),
                ElectionParliamentary.from_year(2004),
                ElectionParliamentary.from_year(2010),
                ElectionParliamentary.from_year(2015),
                ElectionParliamentary.from_year(2020),
            ],
            'Sri Lankan Parliamentary Elections (1989 to 2020)',
        ],
        [
            [
                ElectionPresidential.from_year(1982),
                ElectionPresidential.from_year(1988),
                ElectionPresidential.from_year(1994),
                ElectionPresidential.from_year(1999),
                ElectionPresidential.from_year(2005),
                ElectionPresidential.from_year(2010),
                ElectionPresidential.from_year(2015),
                ElectionPresidential.from_year(2019),
            ],
            'Sri Lankan Presidential Elections (1982 to 2019)',
        ],
        [
            [
                ElectionPresidential.from_year(1982),
                ElectionPresidential.from_year(1988),
                ElectionParliamentary.from_year(1989),
                ElectionParliamentary.from_year(1994),
                ElectionPresidential.from_year(1994),
            ],
            'Jayawardena/Premadasa',
        ],
        [
            [
                ElectionPresidential.from_year(1988),
                ElectionParliamentary.from_year(1989),
                ElectionParliamentary.from_year(1994),
                ElectionPresidential.from_year(1994),
                ElectionPresidential.from_year(1999),
                ElectionParliamentary.from_year(2000),
                ElectionParliamentary.from_year(2001),
                ElectionParliamentary.from_year(2004),
            ],
            'Bandaranaike III',
        ],
        [
            [
                ElectionParliamentary.from_year(2000),
                ElectionParliamentary.from_year(2001),
                ElectionParliamentary.from_year(2004),
                ElectionPresidential.from_year(2005),
                ElectionPresidential.from_year(2010),
                ElectionParliamentary.from_year(2010),
                ElectionPresidential.from_year(2015),
            ],
            'Rajapaksa I',
        ],
        [
            [
                ElectionParliamentary.from_year(2010),
                ElectionPresidential.from_year(2015),
                ElectionParliamentary.from_year(2015),
                ElectionPresidential.from_year(2019),
            ],
            'Sirisena',
        ],
        [
            [
                ElectionParliamentary.from_year(2015),
                ElectionPresidential.from_year(2019),
                ElectionParliamentary.from_year(2020),
            ],
            'Rajapaksa II',
        ],        
    ]:
        MultiStepSankey(
            election_list,
            title,
        ).draw()
