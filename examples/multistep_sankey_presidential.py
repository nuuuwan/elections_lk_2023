from elections_lk import ElectionPresidential, MultiStepSankey

if __name__ == "__main__":
    for election_list, title in [
        [
            [
                # 1980s
                ElectionPresidential.from_year(1982),
                ElectionPresidential.from_year(1988),
                # 1990s
                ElectionPresidential.from_year(1994),
                ElectionPresidential.from_year(1999),
                # 2000s
                ElectionPresidential.from_year(2005),
                # 2010s
                ElectionPresidential.from_year(2010),
                ElectionPresidential.from_year(2015),
                ElectionPresidential.from_year(2019),
                # 2020s
                ElectionPresidential.from_year(2024),
            ],
            "Presidential Elections (1982 - Present)",
        ],
    ]:
        mss = MultiStepSankey(
            election_list,
            title,
        )
        mss.draw()
