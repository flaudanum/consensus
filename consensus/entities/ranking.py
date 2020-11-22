from copy import deepcopy
from enum import Enum, auto
from typing import Sequence

from consensus.entities.alternative import Alternative


class Preference(Enum):
    MODERATE = auto()
    STRONG = auto()
    VERY_STRONG = auto()
    EXTREME = auto()


class Ranking:

    @property
    def sets(self):
        return deepcopy(self._sets)

    @property
    def intensities(self) -> dict[tuple, Preference]:
        return {
            (n + 1, n + 2): intensity
            for n, intensity in enumerate(self._intensities)
        }

    def __init__(self, alternatives: Sequence[Alternative], sets: Sequence[Sequence[str]],
                 intensities: Sequence[Preference] = ()):
        self._sets = sets

        # Register alternatives by name
        self._alternatives_by_name = {}
        for alt in alternatives:
            self._alternatives_by_name[alt.name] = alt

        # Checks preference intensities
        if intensities:
            if len(intensities) != (len(sets) - 1):
                raise ValueError(
                    f"Expected number of intensity specifications is {(len(sets) - 1)}, provided: {len(intensities)}")
            for item in intensities:
                assert isinstance(item, Preference)

        # Intensities of preferences between classes
        self._intensities = intensities

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
