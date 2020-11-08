from typing import Sequence, Optional

from consensus.entities.alternative import Alternative
from consensus.entities.ranking import Ranking


class Member:
    @property
    def name(self):
        return self._name

    @property
    def ranking(self):
        return self._ranking

    def __init__(self, name: str):
        self._name = name
        self._ranking: Optional[Ranking] = None

    def make_ranking(self, alternatives: Sequence[Alternative], ranking: Sequence[Sequence[str]]):
        self._ranking = Ranking(alternatives, ranking)
