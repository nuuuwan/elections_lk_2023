from elections_lk import ElectionPresidential, Sankey

if __name__ == "__main__":
    for election_x, election_y, title, include_others in [
        [
            ElectionPresidential.from_year(1982),
            ElectionPresidential.from_year(1988),
            "1982 and 1988 Sri Lankan Presidential Elections",
            True,
        ],
        [
            ElectionPresidential.from_year(2005),
            ElectionPresidential.from_year(2015),
            "2005 and 2015 Sri Lankan Presidential Elections",
            False,
        ],
        [
            ElectionPresidential.from_year(2019),
            ElectionPresidential.from_year(2024),
            "2019 and 2024 Sri Lankan Presidential Elections",
            True,
        ],
    ]:

        s = Sankey(election_x, election_y, title, include_others)
        s.save_tsv()
        s.save_md()
        s.draw()
