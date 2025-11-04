from utils import Log

from elections_lk.elections.ElectionBase import ElectionBase
from elections_lk.elections.ElectionLoaderMixin import ElectionLoaderMixin

log = Log("Election")


class Election(ElectionBase, ElectionLoaderMixin):
    pass
