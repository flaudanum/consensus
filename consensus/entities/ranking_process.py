from itertools import chain
from typing import Sequence

from consensus.algorithms.base_algo import compute_payoff
from consensus.algorithms.variation_algo import compute_payoff_with_intensities
from consensus.entities.alternative import Alternative
from consensus.entities.member import Member
from consensus.exceptions import PayoffError


class RankingProcess:

    @property
    def alternatives(self):
        return {
            alt.name: {"description": alt.description}
            for alt in self._alternatives
        }

    @property
    def members(self):
        return sorted([member.name for member in self._members])

    def __init__(self):
        self._members: list[Member] = []
        self._alternatives: list[Alternative] = []

    def new_member(self, name) -> None:
        for member in self._members:
            if member.name.lower() == name.lower():
                raise ValueError(f"A member with name '{name}' already exists")

        self._members.append(Member(name))

    def new_alternative(self, name: str, description: str = ""):
        for alt in self._alternatives:
            if alt.name.lower() == name.lower():
                raise ValueError(f"An alternative with name '{name}' already exists")

        self._alternatives.append(Alternative(name, description))

    def _get_member_by_name(self, name):
        for member in self._members:
            if member.name.lower() == name.lower():
                return member
        raise ValueError(f"No member with name '{name}'.")

    def _get_alternative_by_name(self, name):
        for alternative in self._alternatives:
            if alternative.name.lower() == name.lower():
                return alternative
        return None

    def get_ranking(self, name: str):
        member = self._get_member_by_name(name)
        if member.ranking:
            return member.ranking.sets
        else:
            return None

    def make_ranking(self, name: str, ranking: Sequence[Sequence[str]], intensities=()) -> None:
        member = self._get_member_by_name(name)
        # List of names of alternatives provided in the ranking
        alt_names_ranking = chain.from_iterable(ranking)
        if {aname.lower() for aname in alt_names_ranking} != {aname.lower() for aname in self.alternatives}:
            raise ValueError("The ranking mismatch with the set of alternatives.")

        member.make_ranking(
            alternatives=self._alternatives,
            ranking=ranking,
            intensities=intensities
        )

    def payoff(self):
        # ----- Checking prerequisites -----
        # There is at least two members
        if len(self._members) < 2:
            raise PayoffError(f"Computing a payoff requires at least two members: {len(self._members)}")
        # There must be alternatives
        if len(self._alternatives) == 0:
            raise PayoffError("Cannot compute a payoff as no alternatives are specified.")
        # Members must have made rankings
        for member in self._members:
            if not member.ranking:
                raise PayoffError(f"Member '{member.name}' must make a ranking.")

        algo = 'base'

        # Checks variable intensities in preferences have been specified
        for member in self._members:
            if member.ranking.intensities:
                algo = 'intensities'
                break

        # ----- Computing payoff with base algorithm -----
        if algo == 'base':
            return compute_payoff(self._alternatives, self._members)
        elif algo == 'intensities':
            return compute_payoff_with_intensities(self._alternatives, self._members)
        else:
            raise ValueError(f"Unknown algorithm: '{algo}'")
