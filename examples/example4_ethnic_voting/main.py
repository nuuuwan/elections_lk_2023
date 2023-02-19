from gig import Ent
from utils import Log, TSVFile

from elections_lk import (
    ElectionLocalAuthority,
    ElectionParliamentary,
    ElectionPresidential,
)
from examples.example4_ethnic_voting.EthnicVoting import EthnicVoting

TEST_ED_ID = 'EC-01'
log = Log('Ethnic Voting')


def format_p(p):
    return p
    return f'{p:.1%}'


def main():
    d_list = []
    for cls_election in [
        ElectionLocalAuthority,
        ElectionParliamentary,
        ElectionPresidential,
    ]:
        election_type = cls_election.get_election_type()
        for year in cls_election.get_years():
            log.debug(election_type, year)
            election = cls_election.load(year)
            example = EthnicVoting(election)
            winning_party = (
                election.country_final_result.party_to_votes.winning_party
            )
            d_list.append(
                dict(
                    election_type=election_type,
                    winning_party=winning_party,
                    year=year,
                    p_group_effect=example.p_group_effect,
                )
            )

    tsv_path = __file__[:-3] + '.tsv'
    TSVFile(tsv_path).write(d_list)
    log.info(f'Saved {tsv_path}')


def main_model_only():
    election = ElectionPresidential.from_year(2019)
    example = EthnicVoting(election)
    party = 'SLPP'
    index_of_party = example.election.all_parties.index(party)

    d_list = []
    model = example.get_prediction_model()
    for result in example.election.results:
        pd_id = result.region_id
        if TEST_ED_ID not in pd_id:
            continue
        if pd_id[-1] == 'P':
            name = 'Postal Votes'
        else:
            ent = Ent.from_id(pd_id)
            name = ent.name

        x = example.get_x_from_result(result)
        yhat = model.predict([x])[0]

        p_votes = result.get_party_pvotes(party)
        p_votes_predicted = yhat[index_of_party]
        error = p_votes_predicted - p_votes

        d_list.append(
            dict(
                pd_id=pd_id,
                name=name,
                p_votes=p_votes,
                p_votes_predicted=p_votes_predicted,
                error=error,
            )
        )

    tsv_path = __file__[:-3] + '.model.tsv'
    TSVFile(tsv_path).write(d_list)
    log.info(f'Saved {tsv_path}')


if __name__ == '__main__':
    main_model_only()
