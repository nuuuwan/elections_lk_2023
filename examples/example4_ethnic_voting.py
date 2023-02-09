from functools import cached_property

from gig import Ent, GIGTable

from elections_lk import ElectionPresidential, ElectionParliamentary

GIG_TABLE_ETH = GIGTable('population-ethnicity', 'regions', '2012')
# GIG_TABLE_REL =  GIGTable('population-religion', 'regions', '2012')


class EthnicVoting:
    def __init__(self, election):
        self.election = election

    @cached_property
    def country_effect(self):
        return self.election.country_final_result.party_to_votes.dict_p

    @cached_property
    def n(self):
        return len(self.election.pd_results)

    @staticmethod
    def get_group_to_p_from_pd_id(id):
        if id[-1] in ['P', 'D']:
            id = id[:5]  # if postal vote, revert to electoral district

        ent = Ent.from_id(id)
        d_eth = ent.gig(GIG_TABLE_ETH)

        return {
            'sinhala': d_eth.dict_p['sinhalese'],
            'tamil': d_eth.dict_p['sl_tamil'] + d_eth.dict_p['ind_tamil'],
            'muslim': d_eth.dict_p['sl_moor'] + d_eth.dict_p['malay'],
        }

    @cached_property
    def group_to_party_to_votes(self):
        group_to_party_to_votes = {}
        for pd_result in self.election.pd_results:
            group_to_p = self.get_group_to_p_from_pd_id(pd_result.region_id)
            for group, p in group_to_p.items():
                if group not in group_to_party_to_votes:
                    group_to_party_to_votes[group] = {}

                for party, votes in pd_result.party_to_votes.items():
                    group_to_party_to_votes[group][party] = (
                        group_to_party_to_votes[group].get(party, 0)
                        + p * votes
                    )
        return group_to_party_to_votes

    @cached_property
    def group_to_effect(self):
        group_to_effect = {}
        for group, party_to_votes in self.group_to_party_to_votes.items():
            effect = {}
            total_votes = sum(party_to_votes.values())
            for party, votes in party_to_votes.items():
                effect[party] = votes / total_votes
            group_to_effect[group] = effect
        return group_to_effect

    def get_group_effect_from_pd_result(self, pd_result):
        pd_id = pd_result.region_id
        group_to_p = self.get_group_to_p_from_pd_id(pd_id)
        group_effect = 0
        for group, effect in self.group_to_effect.items():
            group_effect += group_to_p.get(group, 0) * effect
        return group_effect

    def get_final_effect_from_pd_result(self, pd_result):
        return pd_result.get_party_pvotes(self.party)

    @cached_property
    def total_variance(self):
        country_effect = self.country_effect
        weighted_total_div_sum2 = 0
        weight_sum = 0
        for pd_result in example.election.pd_results:
            for party, votes in pd_result.party_to_votes.items():
                pvotes = votes / pd_result.total_votes

                total_div = pvotes - country_effect[party]

                weight = pd_result.total_votes * pvotes
                weighted_total_div_sum2 += (total_div**2) * weight
                weight_sum += weight

        return weighted_total_div_sum2 / weight_sum

    @cached_property
    def group_variance(self):
        country_effect = self.country_effect
        group_to_effect = self.group_to_effect

        weighted_total_div_sum2 = 0
        weight_sum = 0
        for pd_result in example.election.pd_results:
            group_to_p = self.get_group_to_p_from_pd_id(pd_result.region_id)
            party_to_predicted_votes = {}
            for group, p in group_to_p.items():
                for party, p_party in group_to_effect[group].items():
                    if party not in party_to_predicted_votes:
                        party_to_predicted_votes[party] = 0

                    party_to_predicted_votes[party] += pd_result.total_votes * p_party * p

            for party, predicted_votes in party_to_predicted_votes.items():
                pvotes = predicted_votes / pd_result.total_votes
                group_div = pvotes - country_effect[party]

                weight = pd_result.total_votes * pvotes           
                weighted_total_div_sum2 += (group_div**2) * weight
                weight_sum += weight

        return weighted_total_div_sum2 / weight_sum

    @cached_property
    def p_group_effect(self):
        return self.group_variance / self.total_variance


def format_p(p):
    return f'{p:.1%}'


if __name__ == '__main__':
    for year in ElectionPresidential.get_years():
        election = ElectionPresidential.load(year)
        example = EthnicVoting(election)
        print(year, format_p(example.p_group_effect))

    for year in ElectionParliamentary.get_years():
        election = ElectionParliamentary.load(year)
        example = EthnicVoting(election)
        print(year, format_p(example.p_group_effect))
