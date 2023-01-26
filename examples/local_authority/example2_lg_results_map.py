import matplotlib.pyplot as plt
from gig import Ent

from elections_lk.elections import ElectionLocalAuthority
from elections_lk.core import Party


if __name__ == '__main__':
    election = ElectionLocalAuthority.load(2018)

    _, ax = plt.subplots(figsize=(10, 16))

    for result in election.lg_final_results:
        best_party, best_seats = result.party_to_seats.items_sorted()[0]
        ent = Ent.from_id(result.region_id)
        if best_seats > result.total_seats / 2:
            color = Party(best_party).color
        else:
            color = '#888'

        ent.geo().plot(ax=ax, color=color)

    plt.axis('off')
    plt.suptitle('2018 Sri Lankan local elections')
    plt.title('Party with Most Votes')

    png_file_name = __file__[:-3] + '.png'
    plt.savefig(png_file_name)
    plt.close()

    print('Saved ', png_file_name)
