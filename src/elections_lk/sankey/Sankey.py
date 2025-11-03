from utils import Log

from elections_lk.sankey.report import SankeyReportMixin
from elections_lk.sankey.SankeyBase import SankeyBase
from elections_lk.sankey.SankeyDrawMixin import SankeyDrawMixin
from elections_lk.sankey.SankeyModelMixin import SankeyModelMixin
from elections_lk.sankey.SankeyModelNormalizeMixin import \
    SankeyModelNormalizeMixin

log = Log("PartyContinuity")


class Sankey(
    SankeyBase,
    SankeyModelMixin,
    SankeyModelNormalizeMixin,
    SankeyReportMixin,
    SankeyDrawMixin,
):
    pass
