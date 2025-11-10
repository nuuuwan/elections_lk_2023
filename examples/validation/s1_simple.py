import random

from elections_lk import (
    ElectionPresidential,
    PartyToVotes,
    Result,
    Sankey,
    SummaryStatistics,
)

N_PDS = 100


class DummyElectionFactory:
    @staticmethod
    def gen_dummy(year):
        results = []
        for i_pd in range(N_PDS):
            electors = random.randint(10_000, 1_000_000)
            p_turnout = random.uniform(0.5, 0.9)
            polled = int(electors * p_turnout)
            p_rejected = random.uniform(0.01, 0.1)
            rejected = int(polled * p_rejected)
            valid = polled - rejected

            party_a_votes = random.randint(int(valid * 0.1), int(valid * 0.9))
            party_b_votes = valid - party_a_votes

            result = Result(
                region_id=f"region_{i_pd:04d}",
                summary_statistics=SummaryStatistics(
                    electors=electors,
                    polled=polled,
                    valid=valid,
                    rejected=rejected,
                ),
                party_to_votes=PartyToVotes(
                    {
                        "A": party_a_votes,
                        "B": party_b_votes,
                    }
                ),
            )
            results.append(result)

        election = ElectionPresidential(
            date=f"{year}-01-01",
            results=results,
        )
        return election

    @staticmethod
    def gen_dummy_from_prev(election_prev, matrix):
        results = []
        for i_pd, result_prev in enumerate(election_prev.results):
            non_votes_prev = (
                result_prev.summary_statistics.electors
                - result_prev.summary_statistics.valid
            )
            party_to_votes_prev = result_prev.party_to_votes
            party_a_votes = (
                party_to_votes_prev["A"] * matrix[0][0]
                + party_to_votes_prev["B"] * matrix[0][1]
                + non_votes_prev * matrix[0][2]
            )
            party_b_votes = (
                party_to_votes_prev["A"] * matrix[1][0]
                + party_to_votes_prev["B"] * matrix[1][1]
                + non_votes_prev * matrix[1][2]
            )
            non_votes = (
                party_to_votes_prev["A"] * matrix[2][0]
                + party_to_votes_prev["B"] * matrix[2][1]
                + non_votes_prev * matrix[2][2]
            )

            valid = party_a_votes + party_b_votes
            electors = valid + non_votes
            summary_statistics_prev = result_prev.summary_statistics
            p_rejected = summary_statistics_prev.p_rejected
            rejected = int((valid / (1 - p_rejected)) * p_rejected)
            polled = valid + rejected

            new_result = Result(
                region_id=result_prev.region_id,
                summary_statistics=SummaryStatistics(
                    electors=electors,
                    polled=polled,
                    valid=valid,
                    rejected=rejected,
                ),
                party_to_votes=PartyToVotes(
                    {
                        "A": party_a_votes,
                        "B": party_b_votes,
                    }
                ),
            )

            results.append(new_result)

        year_prev = int(election_prev.date[:4])
        year = year_prev + 5
        new_election = ElectionPresidential(
            date=f"{year}-01-01",
            results=results,
        )
        return new_election


if __name__ == "__main__":

    for i_matrix, (label, matrix) in enumerate(
        [
            # ["100% All voters loyal", ((1, 0, 0), (0, 1, 0), (0, 0, 1))],
            # ["100% Party Switch", ((0, 1, 0), (1, 0, 0), (0, 0, 1))],
            # [
            #     "50% Party Switch",
            #     ((0.50, 0.50, 0), (0.50, 0.50, 0), (0, 0, 1)),
            # ],
            [
                "25% Party Switch",
                ((0.75, 0.25, 0), (0.25, 0.75, 0), (0, 0, 1)),
            ],
        ],
        start=1,
    ):
        election_1 = DummyElectionFactory.gen_dummy(year=3000 + 10 * i_matrix)
        election_2 = DummyElectionFactory.gen_dummy_from_prev(
            election_1, matrix
        )

        s = Sankey(
            election_1,
            election_2,
            f"Scenario 1.{i_matrix} {label}",
            include_others=False,
        )
        s.save_tsv()
        s.save_md()
        s.draw()
