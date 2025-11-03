from functools import cached_property

import plotly.graph_objects as go
from utils import Log

from elections_lk import Party

log = Log("SankeyDrawDataMixin")


class SankeyDrawDataMixin:
    VOTE_LIMIT = 10_000
    ALPHA = 0.25

    @cached_property
    def node_color(self):
        node_color = []
        for matrix in self.matrices:
            for party_x in matrix:
                node_color.append(Party(party_x).color)
        for party_y in list(matrix.values())[0].keys():
            node_color.append(Party(party_y).color)
        return node_color

    @cached_property
    def label(self):
        label = []
        for matrix in self.matrices:
            for party_x in matrix:
                label.append(party_x)
        for party_y in list(matrix.values())[0].keys():
            label.append(party_y)
        return label

    @cached_property
    def label_to_i(self):
        label_to_i = {}
        i = 0
        for i_matrix, matrix in enumerate(self.matrices):
            for party_x in matrix:
                label_to_i[party_x + "_" + str(i_matrix)] = i
                i += 1

        for party_y in list(matrix.values())[0].keys():
            label_to_i[party_y + "_" + str(i_matrix + 1)] = i
            i += 1
        return label_to_i

    @cached_property
    def source(self):
        source = []
        for i_matrix, matrix in enumerate(self.matrices):
            for party_x in matrix:
                i_x = self.label_to_i[party_x + "_" + str(i_matrix)]
                for party_y in matrix[party_x]:
                    if matrix[party_x][party_y] > self.VOTE_LIMIT:
                        source.append(i_x)
        return source

    @cached_property
    def target(self):
        target = []
        for i_matrix, matrix in enumerate(self.matrices):
            for party_x in matrix:
                for party_y in matrix[party_x]:
                    if matrix[party_x][party_y] > self.VOTE_LIMIT:
                        i_y = self.label_to_i[
                            party_y + "_" + str(i_matrix + 1)
                        ]
                        target.append(i_y)
        return target

    @cached_property
    def value(self):
        value = []
        for matrix in self.matrices:
            for party_x in matrix:
                for party_y in matrix[party_x]:
                    if matrix[party_x][party_y] > self.VOTE_LIMIT:
                        value_i = matrix[party_x][party_y]
                        value.append(value_i)
        return value

    @cached_property
    def link_color(self):
        link_color = []
        for matrix in self.matrices:
            for party_x in matrix:
                for party_y in matrix[party_x]:
                    if matrix[party_x][party_y] > self.VOTE_LIMIT:
                        link_color.append(
                            Party(party_x).color_alpha(self.ALPHA)
                        )
        return link_color

    @cached_property
    def sankey_data(self):
        return [
            go.Sankey(
                node=dict(
                    label=self.label,
                    color=self.node_color,
                ),
                link=dict(
                    source=self.source,
                    target=self.target,
                    value=self.value,
                    color=self.link_color,
                ),
            )
        ]
