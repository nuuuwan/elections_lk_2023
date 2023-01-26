import matplotlib.pyplot as plt
from gig import Ent, EntType

from elections_lk.elections import ElectionLocalAuthority

if __name__ == '__main__':
    election = ElectionLocalAuthority.load(2018)
    lg_ents = Ent.list_from_type(EntType.LG)

    _, ax = plt.subplots(figsize=(9, 16))
    for ent in lg_ents:
        print(ent.id)
        geo = ent.geo()
        color = 'red'
        geo.plot(ax=ax, color=color)

    png_file_name = __file__[:-3] + '.png'
    plt.savefig(png_file_name)
    plt.close()
