import os
from functools import cached_property

import plotly.graph_objects as go
from utils import Log

from elections_lk import Party

log = Log('PartyContinuity')

NOT_COUNTED = '(Didn\'t Vote or Rejected)'
WIDTH = 1200
HEIGHT = 675


class SankeyDraw:
    VOTE_LIMIT = 10_000
    WIDTH = 1200
    HEIGHT = 675

    @property
    def image_file_path(self):
        return os.path.join('/tmp', f'sankey_{self.id}.png')

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
    def label_to_iz(self):
        label_to_ix = {}
        label_to_iy = {}
        i = 0
        for matrix in self.matrices:
            for party_x in matrix:
                label_to_ix[party_x] = i
                i += 1
        for party_y in list(matrix.values())[0].keys():
            label_to_iy[party_y] = i
            i += 1
        return label_to_ix, label_to_iy

    @cached_property
    def label_to_ix(self):
        return self.label_to_iz[0]

    @cached_property
    def label_to_iy(self):
        return self.label_to_iz[1]

    @cached_property
    def source(self):
        source = []
        for matrix in self.matrices:
            for party_x in matrix:
                i_x = self.label_to_ix[party_x]
                for party_y in matrix[party_x]:
                    if matrix[party_x][party_y] > self.VOTE_LIMIT:
                        source.append(i_x)
        return source

    @cached_property
    def target(self):
        target = []
        for matrix in self.matrices:
            for party_x in matrix:
                for party_y in matrix[party_x]:
                    if matrix[party_x][party_y] > self.VOTE_LIMIT:
                        i_y = self.label_to_iy[party_y]
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
                        link_color.append(Party(party_x).color_alpha(0.1))
        return link_color

    def draw(self):
        fig = go.Figure(
            data=[
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
        )

        fig.update_layout(title_text=self.title, font_size=10)
        fig.write_image(self.image_file_path, width=WIDTH, height=HEIGHT)
        log.info(f'Saved {self.image_file_path}')
        os.system(f'open {self.image_file_path}')
