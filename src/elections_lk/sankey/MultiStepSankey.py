from functools import cached_property

from utils import Log

# ElectionParliamentary, ElectionPresidential, ElectionLocalAuthority
from elections_lk import ElectionParliamentary, ElectionPresidential
from elections_lk.sankey.Sankey import Sankey
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDraw import SankeyDraw

log = Log("MultiStepSankey")


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


if __name__ == "__main__":
    for election_list, title in [
        [
            [
                # 1980s
                ElectionPresidential.from_year(1982),
                ElectionPresidential.from_year(1988),
                ElectionParliamentary.from_year(1989),
                # 1990s
                ElectionParliamentary.from_year(1994),
                ElectionPresidential.from_year(1994),
                ElectionPresidential.from_year(1999),
                # 2000s
                ElectionParliamentary.from_year(2000),
                ElectionParliamentary.from_year(2001),
                ElectionParliamentary.from_year(2004),
                ElectionPresidential.from_year(2005),
                # 2010s
                ElectionPresidential.from_year(2010),
                ElectionParliamentary.from_year(2010),
                ElectionPresidential.from_year(2015),
                ElectionParliamentary.from_year(2015),
                ElectionPresidential.from_year(2019),
                # 2020s
                ElectionParliamentary.from_year(2020),
                ElectionPresidential.from_year(2024),
                ElectionParliamentary.from_year(2024),
            ],
            "Presidential and Parliamentary Elections (1982-)",
        ],
    ]:
        mss = MultiStepSankey(
            election_list,
            title,
        )
        mss.draw()
        mss.save()
