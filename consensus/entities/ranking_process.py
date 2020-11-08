from itertools import chain
import pandas as pd
from typing import Sequence

from consensus.entities.alternative import Alternative
from consensus.entities.member import Member
from consensus.exceptions import PayoffError


class RankedClass:
    __slots__ = ("frequency", "rank", "alternatives")

    def __repr__(self):
        return "{" + f"'frequency': {self.frequency}, 'rank': {self.rank}" + "}"


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

    def make_ranking(self, name: str, ranking: Sequence[Sequence[str]]) -> None:
        member = self._get_member_by_name(name)
        # List of names of alternatives provided in the ranking
        alt_names_ranking = chain.from_iterable(ranking)
        if {aname.lower() for aname in alt_names_ranking} != {aname.lower() for aname in self.alternatives}:
            raise ValueError("The ranking mismatch with the set of alternatives.")

        member.make_ranking(
            alternatives=self._alternatives,
            ranking=ranking
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

        # Number of alternatives
        num_alternatives = len(self._alternatives)

        payoff_by_member = {}

        for member in self._members:
            name = member.name
            payoff_by_member[name] = {}
            ranked_classes = []

            for pos, alt_set in enumerate(member.ranking):
                # New class ranking
                rk_class = RankedClass()

                # Set of alternatives in the class
                rk_class.alternatives = alt_set

                # Class' frequency
                rk_class.frequency = len(alt_set) / num_alternatives

                # Class' rank
                rk_class.rank = pos + 1

                ranked_classes.append(rk_class)

            class_payoff = 0.
            for rk_class in reversed(ranked_classes):
                payoff_by_member[name].update({alt.name: class_payoff for alt in rk_class.alternatives})
                class_payoff += rk_class.frequency

        payoff_series = {}
        for name, ranking in payoff_by_member.items():
            payoff_series[name] = pd.Series(ranking)

        series = list(payoff_series.values())
        payoff_series["total"] = series.pop().copy()
        while series:
            payoff_series["total"] += series.pop()

        payoff_table = pd.DataFrame(payoff_series)

        # Sorts the table by alternative name
        payoff_table.sort_index(inplace=True)

        # Then sorts the table by payoff values
        payoff_table.sort_values(by=["total"], ascending=False, inplace=True)

        return payoff_table
