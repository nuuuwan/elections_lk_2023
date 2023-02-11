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
    def label_to_i(self):
        label_to_i = {}
        i = 0
        for i_matrix, matrix in enumerate(self.matrices):
            for party_x in matrix:
                label_to_i[party_x + '_' + str(i_matrix)] = i
                i += 1

        for party_y in list(matrix.values())[0].keys():
            label_to_i[party_y + '_' + str(i_matrix + 1)] = i
            i += 1
        return label_to_i

    @cached_property
    def source(self):
        source = []
        for i_matrix, matrix in enumerate(self.matrices):
            for party_x in matrix:
                i_x = self.label_to_i[party_x + '_' + str(i_matrix)]
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
                            party_y + '_' + str(i_matrix + 1)
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
                        link_color.append(Party(party_x).color_alpha(0.2))
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

    def update_layout(self, fig):
        empty_axis = {'showgrid': False, 'zeroline': False, 'visible': False}
        fig.update_layout(
            title_text=self.title,
            font_family='Gill Sans',
            font_size=15,
            xaxis=empty_axis,
            yaxis=empty_axis,
            plot_bgcolor='rgba(0,0,0,0)',
        )

    def save_image(self, fig):
        fig.write_image(self.image_file_path, width=WIDTH, height=HEIGHT)
        log.info(f'Saved {self.image_file_path}')
        os.system(f'open {self.image_file_path}')

    def annotate(self, fig):
        for i_election, election in enumerate(self.election_list):
            fig.add_annotation(
                x=i_election,
                y=-0.1,
                xref="x",
                yref="paper",
                text=election.short_title,
                showarrow=False,
                align="center",
            )

        fig.add_annotation(
            x=0,
            y=1.05,
            xref="x domain",
            yref="y domain",
            text='Data: elections.gov.lk',
            showarrow=False,
            align="left",
        )

        fig.add_annotation(
            x=0,
            y=1,
            xref="x domain",
            yref="y domain",
            text='Model & Visualization: @nuuuwan',
            showarrow=False,
            align="left",
        )

    def draw(self):
        fig = go.Figure(data=self.sankey_data)
        self.annotate(fig)
        self.update_layout(fig)
        self.save_image(fig)
