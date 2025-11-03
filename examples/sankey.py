from elections_lk import ElectionPresidential, Sankey

if __name__ == "__main__":
    for election_list, title in [
        [
            [
                ElectionPresidential.from_year(2005),
                ElectionPresidential.from_year(2015),
            ],
            "2005 and 2015 Sri Lankan Presidential Elections",
        ],
    ]:

        s = Sankey(election_list, title)
        s.save()
        s.draw()
