from gig import Ent, EntType
from utils import TSVFile

DISTRICT_ID = 'LK-13'


def get_gnd_fp_idx(get_parent_id):
    gnd_ents = Ent.list_from_type(EntType.GND)
    idx = {}

    filtered_gnd_ents = [
        gnd_ent for gnd_ent in gnd_ents if gnd_ent.district_id in DISTRICT_ID
    ]

    for gnd_ent in filtered_gnd_ents:
        parent_id = get_parent_id(gnd_ent)
        if parent_id:
            if parent_id not in idx:
                idx[parent_id] = []
            idx[parent_id].append(gnd_ent.id)

    return idx


def render(id):
    ent = Ent.from_id(id)
    name = ent.name
    return f'{name} ({id})'


def render_iter(ids):
    return ', '.join([render(id) for id in ids])


def build_a_to_b(idx_a, idx_b):
    overlap_idx = {}
    for id_a, fp_a in idx_a.items():
        for id_b, fp_b in idx_b.items():
            if set(fp_a).intersection(set(fp_b)):
                if id_a not in overlap_idx:
                    overlap_idx[id_a] = []
                overlap_idx[id_a].append(id_b)
    return overlap_idx


def build_grid(a_to_b, b_to_a, flip):
    d_list = []
    for id_a in sorted(a_to_b, key=lambda k: len(a_to_b[k]), reverse=flip):
        b_list = a_to_b[id_a]
        n_a = len(b_list)

        for i, id_b in enumerate(sorted(b_list)):
            a_list = b_to_a[id_b]
            n_b = len(a_list)
            if n_b == 1:
                if n_a == 1 and not flip:
                    continue

                a = render(id_a) if (i == 0) else ""
                b = render(id_b)
                if flip:
                    t = '1 to 1' if n_a == 1 else '1 to n'
                    d_list.append(dict(t=t, a=a, b=b))
                else:
                    d_list.append(dict(t='n to 1', b=a, a=b))

            elif not flip and n_a > 1:
                d_list.append(
                    dict(t='n to m', b=render(id_a), a=render(id_b))
                )

    return d_list


if __name__ == '__main__':
    lg_idx = get_gnd_fp_idx(lambda gnd_ent: gnd_ent.lg_id)
    pd_idx = get_gnd_fp_idx(lambda gnd_ent: gnd_ent.pd_id)

    lg_to_pd = build_a_to_b(lg_idx, pd_idx)
    pd_to_lg = build_a_to_b(pd_idx, lg_idx)

    n = len(lg_idx) + len(pd_idx)
    d_list = build_grid(lg_to_pd, pd_to_lg, True) + build_grid(
        pd_to_lg, lg_to_pd, False
    )
    d_list = sorted(d_list, key=lambda k: k['t'])
    TSVFile('temp.tsv').write(d_list)
