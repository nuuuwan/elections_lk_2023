from utils import Log

from elections_lk.core.PARTY_TO_COLOR import PARTY_TO_COLOR, NOT_COUNTED

log = Log('Party')


class Party:
    DEFAULT_COLOR = '#404040'

    def __init__(self, party: str):
        self.party = party

    @property
    def color(self):
        if self.party not in PARTY_TO_COLOR:
            log.error(f'Party {self.party} not found in PARTY_TO_COLOR')
            return Party.DEFAULT_COLOR
        return PARTY_TO_COLOR[self.party]

    def color_alpha(self, alpha):
        color = self.color

        def hex_to_int(hex):
            return int(hex, 16)

        r = hex_to_int(color[1:3])
        g = hex_to_int(color[3:5])
        b = hex_to_int(color[5:7])
        return f'rgba({r}, {g}, {b}, {alpha})'
