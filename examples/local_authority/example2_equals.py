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

    

if __name__ == '__main__':
    lg_idx = get_gnd_fp_idx(lambda gnd_ent: gnd_ent.lg_id)
    pd_idx = get_gnd_fp_idx(lambda gnd_ent: gnd_ent.pd_id)
    dsd_idx = get_gnd_fp_idx(lambda gnd_ent: gnd_ent.dsd_id)

    print(len(lg_idx), len(pd_idx), len(dsd_idx))

    idx_a , idx_b = lg_idx, pd_idx
    
    info_idx = {'equal': [], 'subset': [], 'superset': [], 'other': []}
    for id_a, fp_a in idx_a.items():
        if 'LG-13' not in id_a:
            continue
        
        equals_set = set()
        subsets_set = set()
        supersets_set = set()
        rel_type = 'other'
        for id_b, fp_b in idx_b.items():
            if 'EC-03' not in id_b:
                continue
            
            if fp_a == fp_b:
                equals_set.add(id_b)
                rel_type = 'equal'
            elif set(fp_a).issubset(set(fp_b)):
                subsets_set.add(id_b)
                rel_type = 'subset'
            elif set(fp_b).issubset(set(fp_a)):
                supersets_set.add(id_b)
                rel_type = 'superset'
            

        info_idx[rel_type].append(
            dict(id_a=id_a, equals_set=equals_set, subsets_set=subsets_set, supersets_set=supersets_set)
        )

    def render(id):
        ent = Ent.from_id(id)
        name = ent.name
        return f'{name} ({id})'

    def render_id_set(id_set):
        return ', '.join([render(id) for id in id_set])

    
    for rel_type, info_list in info_idx.items():
        print(f'{rel_type} ({len(info_list)})')
        for info in info_list:
            id_a = info['id_a']
            equals_set = info['equals_set']
            subsets_set = info['subsets_set']
            supersets_set = info['supersets_set']

            label_a = render(id_a)

            if rel_type == 'equal':
                print('\t', label_a, '=', render(list(equals_set)[0]))
            elif rel_type == 'subset':
                print('\t', label_a, '<', render(list(subsets_set)[0]))
            elif rel_type == 'superset':
                print('\t', label_a, '>', render_id_set(list(supersets_set)))
            elif rel_type == 'other':
                print('\t', label_a, '<>')
            else:
                raise ValueError('Unknonw rel_type: ' + rel_type)

        
        


        
        
 
        
