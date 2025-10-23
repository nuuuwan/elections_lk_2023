import os

import plotly.graph_objects as go
from utils import Log

from elections_lk.sankey.SankeyDrawData import SankeyDrawData

log = Log("SankeyDraw")

EMPTY_AXIS = {"showgrid": False, "zeroline": False, "visible": False}


class SankeyDraw(SankeyDrawData):
    VOTE_LIMIT = 10_000
    WIDTH = 1600
    HEIGHT = 900
    P_MARGIN = 0.1
    MARGIN_X = 0.5 * P_MARGIN * WIDTH
    MARGIN_TOP = 1.5 * P_MARGIN * HEIGHT
    MARGIN_BOTTOM = 1.5 * P_MARGIN * HEIGHT

    @property
    def image_file_path(self):
        return os.path.join("/tmp", f"sankey_{self.id}.png")

    def update_layout(self, fig):
        fig.update_layout(
            font_family="Ubuntu",
            font_size=15,
            xaxis=EMPTY_AXIS,
            yaxis=EMPTY_AXIS,
            margin=dict(
                l=self.MARGIN_X,
                r=self.MARGIN_X,
                t=self.MARGIN_TOP,
                b=self.MARGIN_BOTTOM,
            ),
            plot_bgcolor="#ffffff",
        )

    def save_image(self, fig):
        fig.write_image(
            self.image_file_path, width=self.WIDTH, height=self.HEIGHT
        )
        log.info(f"Saved {self.image_file_path}")
        os.system(f"open {self.image_file_path}")

    def annotate(self, fig):
        for i_election, election in enumerate(self.election_list):
            fig.add_annotation(
                x=i_election,
                y=-0.09,
                xref="x",
                yref="paper",
                text=election.year,
                showarrow=False,
                align="center",
                font_size=30,
                font=dict(color="rgba(0,0,0,0.5)"),
            )
            fig.add_annotation(
                x=i_election,
                y=-0.12,
                xref="x",
                yref="paper",
                text=election.get_election_type().title(),
                showarrow=False,
                align="center",
                font_size=15,
                font=dict(color="rgba(0,0,0,0.33)"),
            )

        fig.add_annotation(
            x=0.5,
            y=1.15,
            xref="x domain",
            yref="y domain",
            text=self.title,
            showarrow=False,
            align="center",
            font_size=40,
        )

        fig.add_annotation(
            x=0.5,
            y=-0.18,
            xref="x domain",
            yref="y domain",
            text="data from elections.gov.lk · model & visualization by @nuuuwan",
            showarrow=False,
            align="center",
            font_size=15,
            font=dict(color="rgba(0,0,0,0.2)"),
        )

    def draw(self):
        fig = go.Figure(data=self.sankey_data)
        self.annotate(fig)
        self.update_layout(fig)
        self.save_image(fig)
