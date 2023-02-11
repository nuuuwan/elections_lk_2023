from functools import cached_property

from sklearn.linear_model import LinearRegression
from utils import Log

log = Log('SankeyModel')


class SankeyModel:
    P_LIMIT = 0.01
    NOT_COUNTED = '(Didn\'t Vote or Rejected)'

    def __init__(self, election_x, election_y):
        self.election_x = election_x
        self.election_y = election_y

    @classmethod
    def get_feature_idx(cls, election, election_end):
        popular_parties = election.get_popular_parties(cls.P_LIMIT)
        idx = {}

        results_idx = election_end.results_idx

        for result in election.results:
            id = result.region_id
            if id in ['EC-11D']:
                continue
            if id not in results_idx:
                continue
            d = result.party_to_votes.get_othered_dict(popular_parties)

            x = [d.get(party, 0) for party in popular_parties]
            idx[id] = x

            result_end = results_idx[id]
            not_counted = (
                result_end.summary_statistics.electors
                - result.summary_statistics.valid
            )
            x.append(not_counted)

        return idx

    @classmethod
    def get_sample_weight_idx(cls, election):
        idx = {}
        for result in election.results:
            id = result.region_id
            if id in ['EC-11D']:
                continue
            idx[id] = result.party_to_votes.total
        return idx

    @classmethod
    def get_training_data(cls, election_x, election_y):
        X_idx = cls.get_feature_idx(election_x, election_y)
        Y_idx = cls.get_feature_idx(election_y, election_y)
        sample_weight_idx = cls.get_sample_weight_idx(election_x)

        common_keys = list(sorted(set(X_idx.keys()) & set(Y_idx.keys())))
        X = [X_idx[key] for key in common_keys]
        Y = [Y_idx[key] for key in common_keys]
        sample_weight = [sample_weight_idx[key] for key in common_keys]

        return X, Y, sample_weight

    @classmethod
    def get_model(cls, election_x, election_y):
        X, Y, sample_weight = cls.get_training_data(election_x, election_y)
        model = LinearRegression(positive=True, fit_intercept=False)
        model.fit(X, Y, sample_weight=sample_weight)
        log.debug('LinearRegression model fitted.')
        return model

    @classmethod
    def get_matrix(cls, election_x, election_y):
        model = cls.get_model(election_x, election_y)
        popular_parties_x = election_x.get_popular_parties(cls.P_LIMIT)
        popular_parties_y = election_y.get_popular_parties(cls.P_LIMIT)
        log.debug(f'{popular_parties_x} -> {popular_parties_y}')

        othered_dict_x = election_x.country_final_result.party_to_votes.get_othered_dict(popular_parties_x)

        matrix = {}
        for i_x, party_x in enumerate(popular_parties_x + [cls.NOT_COUNTED]):
            matrix[party_x] = {}

            if party_x == cls.NOT_COUNTED:
                total = election_y.country_final_result.summary_statistics.electors - election_x.country_final_result.summary_statistics.valid
            else:
                total = othered_dict_x.get(
                    party_x,
                    0,
                )
            for i_y, party_y in enumerate(
                popular_parties_y + [cls.NOT_COUNTED]
            ):
                matrix[party_x][party_y] = model.coef_[i_y][i_x] * total

        return matrix

    @cached_property
    def matrix_model(self):
        matrix_x_to_y = self.get_matrix(self.election_x, self.election_y)
        matrix_y_to_x = self.get_matrix(self.election_y, self.election_x)

        matrix = {}
        for party_x in matrix_x_to_y:
            matrix[party_x] = {}
            for party_y in matrix_x_to_y[party_x]:
                matrix[party_x][party_y] = (
                    2 * matrix_x_to_y[party_x][party_y]
                    + 0 * matrix_y_to_x[party_y][party_x]
                ) / 2
        return matrix
