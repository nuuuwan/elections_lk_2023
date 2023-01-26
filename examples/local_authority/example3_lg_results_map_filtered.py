import sys

import matplotlib.pyplot as plt
from gig import Ent

from elections_lk.elections import ElectionLocalAuthority

PARTY_TO_COLOR = {
    'AITC': '#ff0',
    'CWC': '#f80',
    'IG': '#fff',
    'IG2': '#fff',
    'ITAK': '#ff0',
    'JVP': '#f00',
    'SLFP': '#008',
    'SLPP': '#800',
    'UNP': '#0c0',
    'UPFA': '#00f',
}


if __name__ == '__main__':
    election = ElectionLocalAuthority.load(2018)
    id_filter = sys.argv[1]

    _, ax = plt.subplots(figsize=(16, 9))
    for result in election.lg_final_results:
        ent = Ent.from_id(result.region_id)
        if id_filter not in ent.id:
            continue

        best_party, best_seats = result.party_to_seats.items_sorted()[0]

        if best_seats < 0.5 * result.total_seats:
            color = '#ccc'
        else: 
            if best_party in PARTY_TO_COLOR:
                color = PARTY_TO_COLOR[best_party]
            else:
                print(f"'{best_party}': '',")
                color = '#fff'

        geo = ent.geo()
        geo.plot(ax=ax, color=color)

        plt.annotate(
            ent.acronym,
            xy=ent.lnglat,
            xytext=ent.lnglat,
            horizontalalignment='center',
            verticalalignment='center',
        )

    png_file_name = __file__[:-3] + '.' + id_filter + '.png'
    plt.savefig(png_file_name)
    plt.close()
    print('Saved ', png_file_name)
