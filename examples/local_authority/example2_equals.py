from gig import Ent, EntType
from elections_lk.base import SetCompare
from utils import File


def get_gnd_fp_idx(get_parent_id, filter_parent_id):
    gnd_ents = Ent.list_from_type(EntType.GND)
    idx = {}

    filtered_gnd_ents = [
        gnd_ent
        for gnd_ent in gnd_ents
        if (filter_parent_id in gnd_ent.gnd_id)
    ]

    for gnd_ent in filtered_gnd_ents:
        parent_id = get_parent_id(gnd_ent)
        if parent_id:
            if parent_id not in idx:
                idx[parent_id] = set()
            idx[parent_id].add(gnd_ent.id)

    return idx


def render(id):
    ent = Ent.from_id(id)
    ent_type = EntType.from_id(id)
    suffix = ''
    if ent_type == EntType.PD:
        suffix = ' PD'
    elif ent_type == EntType.DISTRICT:
        suffix = ' District'
    elif ent_type == EntType.ED:
        suffix = ' ED'
    elif ent_type == EntType.DSD:
        suffix = ' DSD'

    name = ent.name
    return f'{name}{suffix} ({id})'


def render_set(id_set):
    if len(id_set) == 1:
        return render(list(id_set)[0])
    inner = ', '.join([render(id) for id in id_set])
    return f'{{{inner}}}'


def run_for_filter(parent_filter_id, get_parent_id_a, get_parent_id_b):
    idx_a = get_gnd_fp_idx(get_parent_id_a, parent_filter_id)
    idx_b = get_gnd_fp_idx(get_parent_id_b, parent_filter_id)

    compare = SetCompare(idx_a, idx_b)
    result = compare.do()

    lines = [
        '',
        '# ' + (render(parent_filter_id)),
    ]
    lines.append('')
    for sa, sb in result['equal']:
        if len(sa) > 1 or len(sb) > 1:
            lines.append(f'* **{render_set(sa)} = {render_set(sb)}**')
        else:
            lines.append(f'* {render_set(sa)} = {render_set(sb)}')

    prev_a = None
    for a, b in result['other']:
        if a != prev_a:
            lines.append('')
        lines.append(f'* *{render(a)} ∩ {render(b)}*')
        prev_a = a

    return lines


if __name__ == '__main__':
    lines = run_for_filter(
        'LK',
        lambda gnd_ent: gnd_ent.district_id,
        lambda gnd_ent: gnd_ent.ed_id,
    )

    district_ids = Ent.ids_from_type(EntType.DISTRICT)
    for parent_filter_id in district_ids:
        lines += run_for_filter(
            parent_filter_id,
            lambda gnd_ent: gnd_ent.lg_id,
            lambda gnd_ent: gnd_ent.pd_id,
        )

    File('examples/local_authority/example2_equals.md').write(
        '\n'.join(lines)
    )
