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
    WIDTH = 1200
    HEIGHT = 675

    @property
    def image_file_path(self):
        return os.path.join(
            '/tmp',
            f'sankey_{self.election_x.year}_{self.election_y.year}.png',
        )

    @property
    def title(self):
        return f'{self.election_x.title} to {self.election_y.title}'

    @cached_property
    def node_color(self):
        matrix = self.matrix
        node_color = []
        for party_x in matrix:
            node_color.append(Party(party_x).color)
        for party_y in list(matrix.values())[0].keys():
            node_color.append(Party(party_y).color)
        return node_color

    @cached_property
    def label(self):
        matrix = self.matrix
        label = []
        for party_x in matrix:
            label.append(party_x)
        for party_y in list(matrix.values())[0].keys():
            label.append(party_y)
        return label

    @cached_property
    def label_to_iz(self):
        matrix = self.matrix
        label_to_ix = {}
        label_to_iy = {}
        i = 0
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
        matrix = self.matrix
        source = []
        for party_x in matrix:
            i_x = self.label_to_ix[party_x]
            for party_y in matrix[party_x]:
                value_i = matrix[party_x][party_y]
                if value_i < 10_000:
                    continue

                source.append(i_x)
        return source

    @cached_property
    def target(self):
        matrix = self.matrix
        target = []
        for party_x in matrix:
            for party_y in matrix[party_x]:
                value_i = matrix[party_x][party_y]
                if value_i < 10_000:
                    continue

                i_y = self.label_to_iy[party_y]
                target.append(i_y)
        return target

    @cached_property
    def value(self):
        matrix = self.matrix
        value = []
        for party_x in matrix:
            for party_y in matrix[party_x]:
                value_i = matrix[party_x][party_y]
                if value_i < 10_000:
                    continue
                value.append(value_i)
        return value

    @cached_property
    def link_color(self):
        matrix = self.matrix
        link_color = []
        for party_x in matrix:
            for party_y in matrix[party_x]:
                value_i = matrix[party_x][party_y]
                if value_i < 10_000:
                    continue
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