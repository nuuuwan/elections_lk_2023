import os

import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from utils import Log, TSVFile

from elections_lk import ElectionPresidential, Party

log = Log('PartyContinuity')

P_LIMIT = 0.005
NOT_COUNTED = '(Didn\'t Vote or Rejected)'
WIDTH = 1200
HEIGHT = 675


class PartyContinuity:
    def __init__(self, election_x, election_y):
        self.election_x = election_x
        self.election_y = election_y

    def feature_idx(self, election):
        popular_parties = election.get_popular_parties(P_LIMIT)
        idx = {}
        for result in election.results:
            
            id = result.region_id
            if id in ['EC-11D']:
                continue
            d = result.party_to_votes.dict
            x = [d.get(party, 0) for party in popular_parties]
            idx[id] = x

            did_not_vote = result.summary_statistics.not_counted
            x.append(did_not_vote)

        return idx

    @property
    def X_idx(self):
        return self.feature_idx(self.election_x)

    @property
    def Y_idx(self):
        return self.feature_idx(self.election_y)

    @property
    def sample_weight_idx(self):
        idx = {}
        for result in self.election_x.results:
            id = result.region_id
            if id in ['EC-11D']:
                continue
            idx[id] = result.party_to_votes.total
        return idx

    @property
    def model(self):
        X_idx, Y_idx, sample_weight_idx = self.X_idx, self.Y_idx, self.sample_weight_idx

        common_keys = list(sorted(set(X_idx.keys()) & set(Y_idx.keys())))
        X = [X_idx[key] for key in common_keys]
        Y = [Y_idx[key] for key in common_keys]
        self.sample_weight = [sample_weight_idx[key] for key in common_keys]

        print(common_keys[0], X[0])
        print(common_keys[0], Y[0])

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

        print(election_x.country_final_result.summary_statistics)

        for i_x, party_x in enumerate(popular_parties_x + [NOT_COUNTED]):
            matrix[party_x] = {}

            if party_x == NOT_COUNTED:
                total = election_x.country_final_result.summary_statistics.not_counted
            else:
                total = election_x.country_final_result.party_to_votes.dict.get(
                    party_x,
                    0,
                )
            print(party_x, total)

            for i_y, party_y in enumerate(popular_parties_y + [NOT_COUNTED]):
                matrix[party_x][party_y] = model.coef_[i_y][i_x] * total

        
        for i_x, party_x in enumerate(popular_parties_x):
            expected_total = election_x.country_final_result.party_to_votes.dict.get(
                party_x,
                0,
            )
            actual_total = sum(matrix[party_x][party_y] for party_y in popular_parties_y)
            r = actual_total / expected_total
            print(party_x, actual_total, expected_total, r)
            if r > 0:
                for i_y, party_y in enumerate(popular_parties_y):
                    actual = matrix[party_x][party_y]
                    matrix[party_x][party_y] = actual / r
                    excess  = actual * (1- 1/r)
                    matrix[NOT_COUNTED][party_y] += excess

        for i_y, party_y in enumerate(popular_parties_y):
            if matrix[NOT_COUNTED][party_y] < 0:
                rem = -matrix[NOT_COUNTED][party_y]
                for i_x, party_x in enumerate(popular_parties_x):
                    matrix[party_x][party_y] = max(0, matrix[party_x][party_y] - rem / len(popular_parties_x))
                    rem = max(0, rem - matrix[party_x][party_y])
                    if rem <= 0:
                        break
                matrix[NOT_COUNTED][party_y]  = -rem

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
        link_color = []
        for party_x in matrix:
            i_x = label_to_ix[party_x]
            for party_y in matrix[party_x]:
                value_i = matrix[party_x][party_y]
                if value_i < 10_000:
                    continue
                i_y = label_to_iy[party_y]
                source.append(i_x)
                target.append(i_y)
                value.append(value_i)
                link_color.append(Party(party_x).color_alpha(0.1))

        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        label=label,
                        color=node_color,
                    ),
                    link=dict(
                        source=source,
                        target=target,
                        value=value,
                        color=link_color,
                    ),
                )
            ]
        )

        fig.update_layout(title_text=self.title, font_size=10)
        fig.write_image(self.image_file_path, width=WIDTH, height=HEIGHT)
        log.info(f'Saved {self.image_file_path}')
        os.system(f'open {self.image_file_path}')


if __name__ == '__main__':
    election_x = ElectionPresidential.from_year(2015)
    election_y = ElectionPresidential.from_year(2019)
    report = PartyContinuity(election_x, election_y)
    report.save()
    report.draw()
