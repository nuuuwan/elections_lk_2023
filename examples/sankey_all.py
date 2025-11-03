from elections_lk import ElectionParliamentary, ElectionPresidential, Sankey

if __name__ == "__main__":
    ALL_ELECTIONS = [
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
    ]
    n = len(ALL_ELECTIONS)
    for i in range(n - 1):
        election_x = ALL_ELECTIONS[i]
        election_y = ALL_ELECTIONS[i + 1]
        s = Sankey(election_x, election_y, "")
        s.save_md()
