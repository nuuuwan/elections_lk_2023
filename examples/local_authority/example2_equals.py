import matplotlib.pyplot as plt
from gig import Ent, EntType

from elections_lk.core import Party
from elections_lk.elections import ElectionLocalAuthority

def get_gnd_fp_idx(get_parent_id):
    gnd_ents = Ent.list_from_type(EntType.GND)
    idx = {}
    for gnd_ent in gnd_ents:
        parent_id = get_parent_id(gnd_ent)
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


if __name__ == '__main__':
    lg_idx = get_gnd_fp_idx(lambda gnd_ent: gnd_ent.lg_id)
    pd_idx = get_gnd_fp_idx(lambda gnd_ent: gnd_ent.pd_id)
    dsd_idx = get_gnd_fp_idx(lambda gnd_ent: gnd_ent.dsd_id)

    print(len(lg_idx), len(pd_idx), len(dsd_idx))

    idx_a , idx_b = lg_idx, pd_idx

    FILTER_A = 'LG-13'
    FILTER_B = 'EC-03'
    
    overlap_idx = {}
    info_idx = {'equal': [], 'subset': [], 'superset': [], 'other': []}
    for id_a, fp_a in idx_a.items():
        if FILTER_A not in id_a:
            continue
        
        for id_b, fp_b in idx_b.items():
            if FILTER_B not in id_b:
                continue

            if set(fp_a).intersection(set(fp_b)):
                if id_a not in overlap_idx:
                    overlap_idx[id_a] = set()
                overlap_idx[id_a].add(id_b)

                if id_b not in overlap_idx:
                    overlap_idx[id_b] = set()
                overlap_idx[id_b].add(id_a)


    def print_overlaps(idx_a, filter_id, print_equal=True):
        print('-' * 32)   
        for id_a in idx_a:
            if filter_id not in id_a:
                continue
            overlaps_id_a = overlap_idx.get(id_a, set())            
            if len(overlaps_id_a) == 1:
                id_b = list(overlaps_id_a)[0]
                overlaps_id_b = overlap_idx.get(id_b, set())

                if len(overlaps_id_b) == 1:
                    print(render(id_a), '=', render(id_b))
                else:
                    print(render(id_a), '<', render(id_b))

        print('-' * 8)    
        for id_a in idx_a:
            if filter_id not in id_a:
                continue
            overlaps_id_a = overlap_idx.get(id_a, set())
            if len(overlaps_id_a) > 1:
                is_superset = all([
                    len(overlap_idx.get(id_b, set())) == 1 for id_b in overlaps_id_a
                ])
                if is_superset:
                    print(render(id_a), '=', render_iter(overlaps_id_a))
                else:
                    print(render(id_a), '<>', render_iter(overlaps_id_a))

    print_overlaps(idx_a, FILTER_A)
    print_overlaps(idx_b, FILTER_B, False)
            
    
        
    

        
        


        
        
 
        
