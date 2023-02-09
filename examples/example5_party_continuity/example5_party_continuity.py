import os

import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from utils import Log, TSVFile

from elections_lk import ElectionPresidential

log = Log('PartyContinuity')

P_LIMIT = 0.005


class PartyContinuity:
    def __init__(self, election_x, election_y):
        self.election_x = election_x
        self.election_y = election_y

    @staticmethod
    def features(election):
        popular_parties = election.get_popular_parties(P_LIMIT)
        idx = {}
        for result in election.results:
            id = result.region_id
            d = result.party_to_votes.dict_p
            x = [d.get(party, 0) for party in popular_parties]
            idx[id] = x
        return [idx[id] for id in sorted(idx.keys())]

    @property
    def X(self):
        return self.features(self.election_x)

    @property
    def Y(self):
        return self.features(self.election_y)

    @property
    def sample_weight(self):
        idx = {}
        for result in self.election_x.results:
            idx[result.region_id] = result.party_to_votes.total
        return [idx[id] for id in sorted(idx.keys())]

    @property
    def model(self):
        X, Y = self.X, self.Y
        model = LinearRegression(positive=True, fit_intercept=False)
        model.fit(X, Y, sample_weight=self.sample_weight)
        return model

    @property
    def report_file_path(self):
        return os.path.join(
            'examples',
            'example5_party_continuity',
            f'report_{self.election_x.year}_{self.election_y.year}.tsv',
        )

    @property
    def report_d_list(self):
        model = self.model
        popular_parties_x = self.election_x.get_popular_parties(P_LIMIT)
        popular_parties_y = self.election_y.get_popular_parties(P_LIMIT)
        log.debug(f'{popular_parties_x} -> {popular_parties_y}')

        d_list = []

        for i_x, party_x in enumerate(popular_parties_x):
            d = {'party_x': party_x}
            x = [
                (1 if party == party_x else 0) for party in popular_parties_x
            ]
            yhat = model.predict([x])[0]

            for i_y, party_y in enumerate(popular_parties_y):
                d[party_y] = yhat[i_y]
            d_list.append(d)
        return d_list

    def save(self):
        TSVFile(self.report_file_path).write(self.report_d_list)
        log.info(f'Saved {self.report_file_path}')
        os.system(f'open {self.report_file_path}')

    @property
    def image_file_path(self):
        return os.path.join(
            'examples',
            'example5_party_continuity',
            f'sankey_{self.election_x.year}_{self.election_y.year}.png',
        )

    def draw(self):
        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=["NDF", "UPFA", "NDF", "SLPP", "NMPP"],
                        color="blue",
                    ),
                    link=dict(
                        source=[
                            0,
                            0,
                            1,
                            1,
                        ],
                        target=[2, 4, 3, 4],
                        value=[
                            0.837544922,
                            0.001904294,
                            1.110049477,
                            0.064564766,
                        ],
                    ),
                )
            ]
        )

        fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
        fig.write_image(self.image_file_path)
        log.info(f'Saved {self.image_file_path}')
        os.system(f'open {self.image_file_path}')


if __name__ == '__main__':
    election_x = ElectionPresidential.from_year(2015)
    election_y = ElectionPresidential.from_year(2019)
    report = PartyContinuity(election_x, election_y)
    # report.save()
    report.draw()
