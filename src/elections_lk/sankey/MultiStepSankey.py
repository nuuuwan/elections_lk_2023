from functools import cached_property

from utils import Log

from elections_lk.sankey.Sankey import Sankey
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDrawMixin import SankeyDrawMixin

# ElectionParliamentary, ElectionPresidential, ElectionLocalAuthority


log = Log("MultiStepSankey")


class MultiStepSankey(SankeyDrawMixin, SankeyBase):
    @cached_property
    def matrices(self):
        matrices = []
        for election_x, election_y in zip(
            self.election_list[:-1], self.election_list[1:]
        ):
            sankey = Sankey([election_x, election_y])
            matrices.append(sankey.matrix)
        return matrices
