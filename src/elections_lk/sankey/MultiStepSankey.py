from functools import cached_property

from utils import Log

from elections_lk.sankey.Sankey import Sankey
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDrawMixin import SankeyDrawMixin

# ElectionParliamentary, ElectionPresidential, ElectionLocalAuthority


log = Log("MultiStepSankey")


class MultiStepSankey(SankeyDrawMixin, SankeyBase):

    def __init__(self, election_list, title, include_others):
        super().__init__(
            election_list[0], election_list[-1], title, include_others
        )
        self.__election_list__ = election_list
        self.title = title

    @property
    def election_list(self):
        return self.__election_list__

    @cached_property
    def matrices(self):
        matrices = []
        for election_x, election_y in zip(
            self.election_list[:-1], self.election_list[1:]
        ):
            sankey = Sankey(
                election_x, election_y, self.title, self.include_others
            )
            matrices.append(sankey.matrix)
        return matrices
