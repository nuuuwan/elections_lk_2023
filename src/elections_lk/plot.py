"""Plots."""
import matplotlib.pyplot as plt
from geo import geodata
from elections_lk import presidential
import geoplot
import math

def _plot_presidential(year):
    election_data = presidential.get_election_data(year)

    pd_to_winning_party = {}
    for result in election_data:
        pd_id = result['pd_id']
        by_party = result['by_party']
        winning_party = by_party[0]['party_id']
        pd_to_winning_party[pd_id] = winning_party

    def get_winning_party(pd_id):
        return pd_to_winning_party.get(pd_id)

    def get_color(winning_party):
        if winning_party in ['SLPP']:
            return (0.5, 0, 0)
        if winning_party in ['UPFA', 'PA', 'SLFP']:
            return (0.0, 0, 0.8)
        if winning_party in ['NDF', 'UNP']:
            return (0.1, 0.5, 0)
        if winning_party in ['SLMP']:
            return (1, 0, 0.5)
        if winning_party in ['ACTC']:
            return (1, 0.5, 0)
        return (0.2, 0.2, 0,2)

    gpd_df = geodata.get_region_geodata('LK', 'pd')

    gpd_df['winning_party'] = gpd_df['pd_id'].apply(get_winning_party)
    gpd_df['winning_party_color'] = gpd_df['winning_party'].apply(get_color)

    print(gpd_df)

    gpd_df.plot(
        column='winning_party',
        color=gpd_df['winning_party_color'],
        legend=True,
    )
    plt.axis('off')
    plt.title('%d Sri Lankan Presidential Election' % year)
    plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
    image_file = '/tmp/elections_lk.presidential.%d.png' % year
    plt.savefig(image_file)
    plt.show()

if __name__ == '__main__':
    _plot_presidential(2019)
