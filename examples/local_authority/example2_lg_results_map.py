import matplotlib.pyplot as plt
from gig import Ent

from elections_lk.elections import ElectionLocalAuthority

PARTY_TO_COLOR = {
    'ACMC': '#080',
    'AITC': '#ff0',
    'CWC': '#f80',
    'ELMSP': '#f00',
    'EPDP': '#f00',
    'IG': '#000',
    'IG2': '#000',
    'IG3': '#000',    
    'ITAK': '#ff0',
    'JVP': '#f00',
    'MNA': '#080',
    'NC': '#080',
    'SLFP': '#008',
    'SLMC': '#080',
    'SLPP': '#800',
    'TULF': '#f00',
    'UNP': '#0c0',
    'UPFA': '#00f',
}


if __name__ == '__main__':
    election = ElectionLocalAuthority.load(2018)

    _, ax = plt.subplots(figsize=(10, 16))
    for result in election.lg_final_results:
        best_party, best_seats = result.party_to_seats.items_sorted()[0]

        if best_seats < 0.5 * result.total_seats:
            color = '#ccc'
        else: 
            if best_party in PARTY_TO_COLOR:
                color = PARTY_TO_COLOR[best_party]
            else:
                print(f"'{best_party}': '',")
                color = '#fff'

        lg_id = result.region_id

        ent = Ent.from_id(lg_id)
        geo = ent.geo()
        geo.plot(ax=ax, color=color)

    
    plt.suptitle('2018 Sri Lankan local elections')
    plt.title('Party with Most Votes')

    png_file_name = __file__[:-3] + '.png'
    plt.savefig(png_file_name)
    plt.close()

    print('Saved ', png_file_name)
