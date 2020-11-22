import pandas as pd

from consensus.algorithms import RankedClass


def compute_payoff(alternatives, members):
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

        # Less prefered class payoff
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
