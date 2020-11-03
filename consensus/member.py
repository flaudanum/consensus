from copy import deepcopy
from typing import Sequence, Union

from consensus.alternative import Alternative
from consensus.ranking import Ranking


class Member:

    __names = set()

    @staticmethod
    def get_names():
        return deepcopy(Member.__names)

    @property
    def name(self):
        return self._name

    @property
    def ranking(self):
        return self._ranking

    def __init__(self, name: str):
        # Checks if the name is already used
        if name.lower() in Member.__names:
            raise ValueError(f"A member with name '{name}' already exists")
        else:
            Member.__names.add(name.lower())
        self._name = name
        self._ranking: Union[None, Ranking] = None

    def __del__(self):
        if hasattr(self, '_name'):
            Member.__names.remove(self._name.lower())

    def make_ranking(self, alternatives: Sequence[Alternative], ranking: Sequence[Sequence[str]]):
        self._ranking = Ranking(alternatives, ranking)
