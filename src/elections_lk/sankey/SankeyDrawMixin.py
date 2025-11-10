import plotly.graph_objects as go
from utils import Log

from elections_lk.sankey.SankeyDrawDataMixin import SankeyDrawDataMixin

log = Log("SankeyDrawMixin")

EMPTY_AXIS = {"showgrid": False, "zeroline": False, "visible": False}


class SankeyDrawMixin(SankeyDrawDataMixin):
    VOTE_LIMIT = 10_000
    WIDTH = 2400
    HEIGHT = int(WIDTH * 9 / 16)
    P_MARGIN = 0.1
    MARGIN_X = 0.5 * P_MARGIN * WIDTH
    MARGIN_TOP = 1.5 * P_MARGIN * HEIGHT
    MARGIN_BOTTOM = 1.5 * P_MARGIN * HEIGHT

    @property
    def image_file_path(self):
        return self.file_base + ".png"

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

    def __annotate_election_title_in_footer__(
        self, fig, i_election, election
    ):
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

    def annotate(self, fig):
        for i_election, election in enumerate(self.election_list):
            self.__annotate_election_title_in_footer__(
                fig, i_election, election
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
            y=1.075,
            xref="x domain",
            yref="y domain",
            text=" · ".join(
                [
                    "no vote = Eligible voters minus total valid votes cast",
                    f"others = Parties receiving less than {
                        self.P_OTHER_LIMIT:.0%} of the national vote",
                ]
            ),
            showarrow=False,
            align="center",
            font_size=30,
            font=dict(color="rgba(0,0,0,0.4)"),
        )
        fig.add_annotation(
            x=0.5,
            y=-0.18,
            xref="x domain",
            yref="y domain",
            text=" · ".join(
                [
                    "Data Source: Election Commission of Sri Lanka (elections.gov.lk)",
                    "Model and visualisation by Nuwan I. Senaratna (@nuuuwan)",
                ]
            ),
            showarrow=False,
            align="center",
            font_size=30,
            font=dict(color="rgba(0,0,0,0.4)"),
        )

    def draw(self):
        fig = go.Figure(data=self.sankey_data)
        self.annotate(fig)
        self.update_layout(fig)
        self.save_image(fig)
