import sys

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from gig import Ent

from elections_lk.core import Party
from elections_lk.elections import ElectionLocalAuthority

if __name__ == '__main__':
    election = ElectionLocalAuthority.load(2018)
    id_filter = sys.argv[1]

    _, ax = plt.subplots(figsize=(16, 9))

    filtered_results = [
        result
        for result in election.lg_final_results
        if id_filter in result.region_id
    ]
    party_set = set()
    show_labels = len(filtered_results) <= 10
    for result in filtered_results:
        ent = Ent.from_id(result.region_id)
        best_party, best_seats = result.party_to_seats.items_sorted()[0]

        if best_seats > result.total_seats / 2:
            color = Party(best_party).color
            party_set.add(best_party)
        else:
            color = Party.DEFAULT_COLOR
            party_set.add('No Majority')

        plot = ent.geo().plot(ax=ax, color=color)

        if show_labels:
            plt.annotate(
                ent.acronym,
                xy=ent.lnglat,
                xytext=ent.lnglat,
                horizontalalignment='center',
                verticalalignment='center',
            )

    handles = [
        mpatches.Patch(color=Party(party).color, label=party)
        for party in sorted(party_set)
    ]
    plt.legend(handles=handles)

    plt.axis('off')
    plt.suptitle('2018 Sri Lankan local elections')
    plt.title('Party with Most Votes')

    png_file_name = __file__[:-3] + '.' + id_filter + '.png'
    plt.savefig(png_file_name)
    plt.close()

    print('Saved ', png_file_name)
