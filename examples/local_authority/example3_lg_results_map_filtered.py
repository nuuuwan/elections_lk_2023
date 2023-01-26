import sys

import matplotlib.pyplot as plt
from gig import Ent

from elections_lk.elections import ElectionLocalAuthority

from elections_lk.core import Party

if __name__ == '__main__':
    election = ElectionLocalAuthority.load(2018)
    id_filter = sys.argv[1]

    _, ax = plt.subplots(figsize=(16, 9))
    for result in election.lg_final_results:
        ent = Ent.from_id(result.region_id)
        if id_filter not in ent.id:
            continue

        best_party, best_seats = result.party_to_seats.items_sorted()[0]
        ent.geo().plot(ax=ax, color=Party(best_party).color)

        plt.annotate(
            ent.acronym,
            xy=ent.lnglat,
            xytext=ent.lnglat,
            horizontalalignment='center',
            verticalalignment='center',
        )

    plt.suptitle('2018 Sri Lankan local elections')
    plt.title('Party with Most Votes')

    png_file_name = __file__[:-3] + '.' + id_filter + '.png'
    plt.savefig(png_file_name)
    plt.close()
    print('Saved ', png_file_name)
