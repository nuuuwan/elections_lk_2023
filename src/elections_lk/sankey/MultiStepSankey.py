from functools import cached_property

from utils import Log

from elections_lk.sankey.Sankey import Sankey
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDrawMixin import SankeyDraw

# ElectionParliamentary, ElectionPresidential, ElectionLocalAuthority


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
