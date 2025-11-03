from elections_lk.elections.Election import Election
from elections_lk.elections.ElectionLocalAuthority import \
    ElectionLocalAuthority
from elections_lk.elections.ElectionParliamentary import ElectionParliamentary
from elections_lk.elections.ElectionPresidential import ElectionPresidential


class ElectionHistory:
    @property
    def all(self) -> list[Election]:
        return [
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
            ElectionLocalAuthority.from_year(2018),
            ElectionPresidential.from_year(2019),
            # 2020s
            ElectionParliamentary.from_year(2020),
        ]
