from copy import deepcopy
from typing import Sequence

from consensus.entities.alternative import Alternative


class Ranking:

    @property
    def sets(self):
        return deepcopy(self._sets)

    def __init__(self, alternatives: Sequence[Alternative], sets: Sequence[Sequence[str]]):
        self._sets = sets

        # Register alternatives by name
        self._alternatives_by_name = {}
        for alt in alternatives:
            self._alternatives_by_name[alt.name] = alt

        # For iterations
        self._iter_sets = list(self._sets)

    def __iter__(self):
        # returning __iter__ object
        return self

    def __next__(self):
        if not self._iter_sets:
            self._iter_sets = list(self._sets)
            raise StopIteration

        iter_set = self._iter_sets.pop(0)
        return [self._alternatives_by_name[alt_name] for alt_name in iter_set]

    def __str__(self):
        tuples = [tuple(item) for item in self._sets]
        return str(tuple(tuples))
