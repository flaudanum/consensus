from typing import Sequence

import pandas as pd
from math import exp, log

from consensus.algorithms import RankedClass
from consensus.entities.alternative import Alternative
from consensus.entities.member import Member
from consensus.entities.ranking import Preference


def compute_payoff_with_intensities(alternatives: Sequence[Alternative], members: Sequence[Member], ratio_a_ext: float = 10.):
    # Number of alternatives
    num_alternatives = len(alternatives)

    payoff_by_member = {}

    for member in members:
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

        # Exponential coefficient
        alpha = 1. / 3. * log(ratio_a_ext)

        # Categorical specification of intensities of comparisons
        preference_intensities = member.ranking.intensities

        # Less preferred class payoff
        class_payoff = 0.
        for rk_class in reversed(ranked_classes):
            payoff_by_member[name].update({alt.name: class_payoff for alt in rk_class.alternatives})
            class_payoff += rk_class.frequency

            # Stops when reaching the first class
            if rk_class.rank == 1:
                break

            # Gets the intensity $I_c$ of comparison between the current classes and the next prefered one
            if preference_intensities:
                int_index = {
                    Preference.MODERATE: 0.,
                    Preference.STRONG: 1.,
                    Preference.VERY_STRONG: 2.,
                    Preference.EXTREME: 3.
                }[preference_intensities[(rk_class.rank-1, rk_class.rank)]]
            else:
                # Default intensity is MODERATE
                int_index = 0.

            # Preference ratio $a(I_c)$
            ratio_a = exp(alpha * int_index)

            # Additional term representing the increase in intensity of preferences $\varphi_{k,k+1}$
            class_payoff += (ratio_a - 1.) * rk_class.frequency

        # Corrective scaling factor $S$
        scaling_factor = class_payoff

        # Rescales payoffs
        payoff_by_member[name] = {
            alt_name: payoff / scaling_factor
            for alt_name, payoff in payoff_by_member[name].items()
        }

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
