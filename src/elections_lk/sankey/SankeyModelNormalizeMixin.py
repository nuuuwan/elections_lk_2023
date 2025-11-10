import math
from functools import cached_property

from utils import Log

log = Log("SankeyModel")


class SankeyModelNormalizeMixin:
    def analyze_x(self, matrix):
        total = (
            self.election_y.country_final_result.summary_statistics.electors
        )
        final_result_x = self.election_x.country_final_result
        popular_parties_x = self.election_x.get_popular_parties(
            self.P_OTHER_LIMIT, self.include_others
        )
        popular_parties_y = self.election_y.get_popular_parties(
            self.P_OTHER_LIMIT, self.include_others
        )

        correction_factor_idx = {}
        for party_x in popular_parties_x + [self.NO_VOTE]:
            othered_dict_x = final_result_x.party_to_votes.get_othered_dict(
                popular_parties_x, self.include_others
            )

            p_matrix = 0
            for party_y in popular_parties_y + [self.NO_VOTE]:
                p_matrix += matrix[party_x][party_y]

            if party_x == self.NO_VOTE:
                p_actual = (
                    total - final_result_x.summary_statistics.valid
                ) / total
            else:
                p_actual = othered_dict_x.get(party_x, 0) / total

            correction_factor = p_actual / p_matrix
            if math.isnan(correction_factor):
                correction_factor = 1
            correction_factor_idx[party_x] = correction_factor
        return correction_factor_idx

    def analyze_y(self, matrix):
        total = (
            self.election_y.country_final_result.summary_statistics.electors
        )
        final_result_y = self.election_y.country_final_result
        popular_parties_x = self.election_x.get_popular_parties(
            self.P_OTHER_LIMIT, self.include_others
        )
        popular_parties_y = self.election_y.get_popular_parties(
            self.P_OTHER_LIMIT, self.include_others
        )

        correction_factor_idx = {}
        for party_y in popular_parties_y + [self.NO_VOTE]:
            othered_dict_y = final_result_y.party_to_votes.get_othered_dict(
                popular_parties_y, self.include_others
            )

            p_matrix = 0
            for party_x in popular_parties_x + [self.NO_VOTE]:
                p_matrix += matrix[party_x][party_y]

            if party_y == self.NO_VOTE:
                p_actual = (
                    total - final_result_y.summary_statistics.valid
                ) / total
            else:
                p_actual = othered_dict_y.get(party_y, 0) / total

            correction_factor = p_actual / p_matrix
            if math.isnan(correction_factor):
                correction_factor = 1
            correction_factor_idx[party_y] = correction_factor
        return correction_factor_idx

    def normalize_x(self, matrix, correction_factor_idx):
        for party_x in matrix:
            for party_y in matrix[party_x]:
                matrix[party_x][party_y] *= correction_factor_idx[party_x]
        return matrix

    def normalize_y(self, matrix, correction_factor_idx):
        for party_x in matrix:
            for party_y in matrix[party_x]:
                matrix[party_x][party_y] *= correction_factor_idx[party_y]
        return matrix

    @cached_property
    def pmatrix_model(self):
        matrix = self.pmatrix_model_unnormalized

        self.analyze_x(matrix)
        self.analyze_y(matrix)
        for __ in range(self.N_NORMALIZATION_ITERATIONS):
            correction_factor_idx = self.analyze_x(matrix)
            matrix = self.normalize_x(matrix, correction_factor_idx)
            correction_factor_idx = self.analyze_y(matrix)
            matrix = self.normalize_y(matrix, correction_factor_idx)
        self.analyze_x(matrix)
        self.analyze_y(matrix)

        total = sum([sum(row.values()) for row in matrix.values()])
        assert (
            abs(total - 1.0) < 1e-2
        ), f"Total probability not equal to 1 but {total}"
        return matrix

    @cached_property
    def matrix(self):
        pmatrix = self.pmatrix_model
        matrix = {}
        total = (
            self.election_y.country_final_result.summary_statistics.electors
        )
        for party_x in pmatrix:
            matrix[party_x] = {}
            for party_y in pmatrix[party_x]:
                matrix[party_x][party_y] = pmatrix[party_x][party_y] * total
        return matrix

    @cached_property
    def matrices(self):
        return [self.matrix]
