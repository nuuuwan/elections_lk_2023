from functools import cached_property

from sklearn.linear_model import LinearRegression
from utils import Log

from elections_lk.core.Party import NOT_COUNTED

log = Log("SankeyModel")


class SankeyModelMixin:

    N_NORMALIZATION_ITERATIONS = 5
    NOT_COUNTED = NOT_COUNTED

    @classmethod
    def get_feature_idx(cls, election, election_end, include_others):
        popular_parties = election.get_popular_parties(
            cls.P_OTHER_LIMIT, include_others
        )
        idx = {}

        results_idx = election_end.results_idx
        for result in election.results:
            region_id = result.region_id
            if region_id in ["EC-11D"]:
                continue
            if region_id not in results_idx:
                continue

            result_end = results_idx[region_id]
            total = result_end.summary_statistics.electors
            if total < 10:
                continue

            d = result.party_to_votes.get_othered_dict(
                popular_parties, include_others
            )
            p_not_counted = (total - result.summary_statistics.valid) / total

            x = [d.get(party, 0) / total for party in popular_parties] + [
                p_not_counted
            ]
            idx[region_id] = x

        return idx

    @classmethod
    def get_sample_weight_idx(cls, election):
        idx = {}
        for result in election.results:
            id = result.region_id
            if id in ["EC-11D"]:
                continue
            idx[id] = result.summary_statistics.electors
        return idx

    @classmethod
    def get_training_data(
        cls, election_x, election_y, election_end, include_others
    ):
        X_idx = cls.get_feature_idx(election_x, election_end, include_others)
        Y_idx = cls.get_feature_idx(election_y, election_end, include_others)
        sample_weight_idx = cls.get_sample_weight_idx(election_end)

        common_keys = list(sorted(set(X_idx.keys()) & set(Y_idx.keys())))
        X = [X_idx[key] for key in common_keys]
        Y = [Y_idx[key] for key in common_keys]
        sample_weight = [sample_weight_idx[key] for key in common_keys]

        return X, Y, sample_weight

    @classmethod
    def get_trained_model(
        cls, election_x, election_y, election_end, include_others
    ):
        X, Y, sample_weight = cls.get_training_data(
            election_x, election_y, election_end, include_others
        )
        n = len(X)
        assert n == len(Y)
        nX = len(X[0])
        nY = len(Y[0])
        positive = True
        fit_intercept = False
        model = LinearRegression(positive=True, fit_intercept=False)
        model.fit(X, Y, sample_weight=sample_weight)
        log.debug(
            f"LinearRegression fitted ({positive=}, {fit_intercept=},"
            + f" {n=}, {nX=}, {nY=})."
        )
        return model

    @classmethod
    def get_matrix(cls, election_x, election_y, election_end, include_others):
        model = cls.get_trained_model(
            election_x, election_y, election_end, include_others
        )
        popular_parties_x = election_x.get_popular_parties(
            cls.P_OTHER_LIMIT, include_others
        )
        popular_parties_y = election_y.get_popular_parties(
            cls.P_OTHER_LIMIT, include_others
        )

        othered_dict_x = (
            election_x.country_final_result.party_to_votes.get_othered_dict(
                popular_parties_x, include_others
            )
        )

        total = election_end.country_final_result.summary_statistics.electors

        matrix = {}
        for i_x, party_x in enumerate(popular_parties_x + [cls.NOT_COUNTED]):
            matrix[party_x] = {}

            if party_x == cls.NOT_COUNTED:
                total_x = (
                    total
                    - election_x.country_final_result.summary_statistics.valid
                )
            else:
                total_x = othered_dict_x.get(party_x, 0)

            p_x = total_x / total

            for i_y, party_y in enumerate(
                popular_parties_y + [cls.NOT_COUNTED]
            ):
                matrix[party_x][party_y] = p_x * model.coef_[i_y][i_x]

        return matrix

    @cached_property
    def pmatrix_model_unnormalized(self):
        matrix_x_to_y = self.get_matrix(
            self.election_x,
            self.election_y,
            self.election_y,
            self.include_others,
        )
        matrix_y_to_x = self.get_matrix(
            self.election_y,
            self.election_x,
            self.election_y,
            self.include_others,
        )

        PXY = 0.5
        PYX = 1 - PXY

        matrix = {}
        for party_x, party_y_vector in matrix_x_to_y.items():
            matrix[party_x] = {}
            for party_y in party_y_vector:
                matrix[party_x][party_y] = (
                    PXY * matrix_x_to_y[party_x][party_y]
                    + PYX * matrix_y_to_x[party_y][party_x]
                )
        return matrix
