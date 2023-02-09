import os

import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from utils import Log, TSVFile

from elections_lk import ElectionPresidential, Party

log = Log('PartyContinuity')

P_LIMIT = 0.005
NOT_VOTED = '(Not Voted)'


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
            d = result.party_to_votes.dict
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
    def matrix(self):
        model = self.model
        popular_parties_x = self.election_x.get_popular_parties(P_LIMIT)
        popular_parties_y = self.election_y.get_popular_parties(P_LIMIT)
        log.debug(f'{popular_parties_x} -> {popular_parties_y}')

        matrix = {}

        for i_x, party_x in enumerate(popular_parties_x):
            matrix[party_x] = {}
            total = election_x.country_final_result.party_to_votes.dict.get(
                party_x,
                0,
            )
            for i_y, party_y in enumerate(popular_parties_y):
                matrix[party_x][party_y] = model.coef_[i_y][i_x] * total

        not_visited_y = {}
        for party_y in popular_parties_y:
            not_visited_y[party_y] = 0
        not_visited_y[NOT_VOTED] = 0

        for party_x in popular_parties_x:
            total_x = election_x.country_final_result.party_to_votes.dict.get(
                party_x,
                0,
            )
            total_y = sum(matrix[party_x].values())
            not_visited_x = max(total_x - total_y, 0)
            matrix[party_x][NOT_VOTED] = not_visited_x

            if total_y > total_x:
                r = total_x / total_y
                for party_y in popular_parties_y:
                    val = matrix[party_x][party_y]
                    matrix[party_x][party_y] = val * r
                    not_visited_y[party_y] = val * (1 - r)

        matrix[NOT_VOTED] = not_visited_y
        return matrix

    @property
    def d_list(self):
        matrix = self.matrix
        d_list = []
        for party_x in matrix:
            d = {'party': party_x}
            for party_y, value in matrix[party_x].items():
                d[party_y] = round(value, 0)
            d_list.append(d)
        return d_list

    def save(self):
        TSVFile(self.report_file_path).write(self.d_list)
        log.info(f'Saved {self.report_file_path}')
        os.system(f'open {self.report_file_path}')

    @property
    def image_file_path(self):
        return os.path.join(
            'examples',
            'example5_party_continuity',
            f'sankey_{self.election_x.year}_{self.election_y.year}.png',
        )

    @property
    def title(self):
        return f'{self.election_x.title} to {self.election_y.title}'

    def draw(self):
        matrix = self.matrix
        label = []

        i = 0
        label_to_ix = {}
        node_color = []
        for party_x in matrix:
            label.append(party_x)
            label_to_ix[party_x] = i
            i += 1
            node_color.append(Party(party_x).color)

        label_to_iy = {}
        for party_y in list(matrix.values())[0].keys():
            label.append(party_y)
            label_to_iy[party_y] = i
            i += 1
            node_color.append(Party(party_y).color)

        print(label)

        source = []
        target = []
        value = []
        color = []
        for party_x in matrix:
            i_x = label_to_ix[party_x]
            for party_y in matrix[party_x]:
                i_y = label_to_iy[party_y]
                source.append(i_x)
                target.append(i_y)
                value.append(matrix[party_x][party_y])
                color.append('red')

        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=label,
                        color=color,
                    ),
                    link=dict(
                        source=source,
                        target=target,
                        value=value,
                        color=color,
                    ),
                )
            ]
        )

        fig.update_layout(title_text=self.title, font_size=10)
        fig.write_image(self.image_file_path)
        log.info(f'Saved {self.image_file_path}')
        os.system(f'open {self.image_file_path}')


if __name__ == '__main__':
    election_x = ElectionPresidential.from_year(2015)
    election_y = ElectionPresidential.from_year(2019)
    report = PartyContinuity(election_x, election_y)
    # report.save()
    report.draw()
