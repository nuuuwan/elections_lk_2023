from utils import Log

# ElectionParliamentary, ElectionPresidential
from elections_lk import Election, ElectionParliamentary, ElectionPresidential

log = Log('PartyContinuity')


class MultiStepSankey:
    def __init__(self, election_list: list[Election]):
        self.election_list = election_list

    def draw(self):
        pass


if __name__ == '__main__':
    election_list = [
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
        # ElectionPresidential.from_year(2005),
        # 2010s
        # ElectionPresidential.from_year(2010),
        # ElectionParliamentary.from_year(2010),
        # ElectionPresidential.from_year(2015),
        # ElectionParliamentary.from_year(2015),
        # ElectionLocalAuthority.from_year(2018),
        ElectionPresidential.from_year(2019),
        # 2020s
        ElectionParliamentary.from_year(2020),
    ]

    s = MultiStepSankey(election_list)
    s.draw()
