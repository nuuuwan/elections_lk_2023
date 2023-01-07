from dataclasses import dataclass


@dataclass
class SummaryStatistics:
    valid: int
    rejected: int
    polled: int
    electors: int

    @property
    def p_rejected(self):
        return self.rejected / self.polled

    @property
    def p_valid(self):
        return self.valid / self.polled

    @property
    def p_turnout(self):
        return self.polled / self.electors
