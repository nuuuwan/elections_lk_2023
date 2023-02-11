from functools import cached_property

from gig import Ent, GIGTable
from sklearn.linear_model import LinearRegression
from utils import Log

GIG_TABLE_ETH = GIGTable('population-ethnicity', 'regions', '2012')
GIG_TABLE_REL = GIGTable('population-religion', 'regions', '2012')

TEST_ED_ID = 'EC-01'
log = Log('Ethnic Voting')


class EthnicVoting:
    def __init__(self, election):
        self.election = election

    @cached_property
    def country_effect(self):
        return self.election.country_final_result.party_to_votes.dict_p

    @cached_property
    def n(self):
        return len(self.election.results)

    @staticmethod
    def get_group_to_p_from_region_id(id):
        if id[-1] in ['P', 'D']:
            id = id[:5]  # if postal vote, revert to electoral district

        ent = Ent.from_id(id)
        d_eth = ent.gig(GIG_TABLE_ETH)
        ent.gig(GIG_TABLE_REL)

        return {
            'sinhala': d_eth.dict_p['sinhalese'],
            'tamil': d_eth.dict_p['sl_tamil'] + d_eth.dict_p['ind_tamil'],
            'muslim': d_eth.dict_p['sl_moor'] + d_eth.dict_p['malay'],
        }

    @cached_property
    def group_to_party_to_votes(self):
        group_to_party_to_votes = {}
        for result in self.election.results:
            group_to_p = self.get_group_to_p_from_region_id(result.region_id)
            for group, p in group_to_p.items():
                if group not in group_to_party_to_votes:
                    group_to_party_to_votes[group] = {}

                for party, votes in result.party_to_votes.items():
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

    def get_group_effect_from_result(self, result):
        region_id = result.region_id
        group_to_p = self.get_group_to_p_from_region_id(region_id)
        group_effect = 0
        for group, effect in self.group_to_effect.items():
            group_effect += group_to_p.get(group, 0) * effect
        return group_effect

    def get_final_effect_from_result(self, result):
        return result.get_party_pvotes(self.party)

    @cached_property
    def total_variance(self):
        country_effect = self.country_effect
        weighted_total_div_sum2 = 0
        weight_sum = 0
        for result in self.election.results:
            for party, votes in result.party_to_votes.items():
                pvotes = votes / result.total_votes
                total_div = pvotes - country_effect[party]

                weight = result.total_votes * pvotes
                weighted_total_div_sum2 += (total_div**2) * weight
                weight_sum += weight

        return weighted_total_div_sum2 / weight_sum

    def get_x_from_result(self, result):
        group_to_p = self.get_group_to_p_from_region_id(result.region_id)
        return [x[1] for x in sorted(group_to_p.items(), key=lambda x: x[0])]

    def get_y_from_result(self, result):
        return [
            result.get_party_pvotes(party)
            for party in self.election.all_parties
        ]

    def get_prediction_model(self):
        X, Y = [], []
        for result in self.election.results:
            x = self.get_x_from_result(result)
            y = self.get_y_from_result(result)
            X.append(x)
            Y.append(y)

        model = LinearRegression()
        model.fit(X, Y)
        return model

    @cached_property
    def group_variance(self):
        country_effect = self.country_effect
        # group_to_effect = self.group_to_effect

        weighted_total_div_sum2 = 0
        weight_sum = 0

        model = self.get_prediction_model()
        all_parties = self.election.all_parties

        for result in self.election.results:
            self.get_group_to_p_from_region_id(result.region_id)
            x = self.get_x_from_result(result)
            yhat = model.predict([x])[0]
            party_to_predicted_p_votes = {
                party: yhat[i] for i, party in enumerate(all_parties)
            }

            for party, pvotes in party_to_predicted_p_votes.items():
                group_div = pvotes - country_effect[party]

                weight = result.total_votes * pvotes
                weighted_total_div_sum2 += (group_div**2) * weight
                weight_sum += weight

        return weighted_total_div_sum2 / weight_sum

    @cached_property
    def p_group_effect(self):
        return self.group_variance / self.total_variance
