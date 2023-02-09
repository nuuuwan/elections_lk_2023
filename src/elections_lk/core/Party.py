COLOR_TO_PARTY_LIST = {
    '#008800': ['ACMC', 'MNA', 'NC', 'SLMC'],
    '#ffff00': ['AITC', 'ITAK'],
    '#ff8800': ['CWC'],
    '#ff0000': ['ELMSP', 'EPDP', 'JVP', 'TULF', 'NMPP'],
    '#e0e0e0': ['IG', 'IG2', 'IG3'],    
    '#000088': ['SLFP', 'PA','UPFA'],
    '#880000': ['SLPP'],
    '#008800': ['NDF', 'UNP'],
    '#c0c0c0': ['(Not Voted)'],
}

PARTY_TO_COLOR = {}
for color, party_list in COLOR_TO_PARTY_LIST.items():
    for party in party_list:
        PARTY_TO_COLOR[party] = color


class Party:
    DEFAULT_COLOR = '#c0c0c0'

    def __init__(self, party: str):
        self.party = party

    @property
    def color(self):
        return PARTY_TO_COLOR.get(self.party, Party.DEFAULT_COLOR)

    def color_alpha(self, alpha):
        color = self.color
        def hex_to_int(hex):
            return int(hex, 16)
        r = hex_to_int(color[1:3])
        g = hex_to_int(color[3:5])
        b = hex_to_int(color[5:7])
        return f'rgba({r}, {g}, {b}, {alpha})'
