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

DEFAULT_PARTY_COLOR = '#888'

class Party:
    def __init__(self, party: str):
        self.party = party

    @property
    def color(self):
        return PARTY_TO_COLOR.get(self.party, DEFAULT_PARTY_COLOR)
        