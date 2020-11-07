from consensus.entities.group import Group


class RankedClass:
    __slots__ = ("frequency", "rank", "payoff", "alternatives")

    def __repr__(self):
        return "{" + f"'frequency': {self.frequency}, 'rank': {self.rank}, 'payoff': {self.payoff}" + "}"


def payoff(group: Group):
    num_alternatives = group.num_alternatives

    payoff_by_member_name = {}
    payoff_global = []

    for name, member in sorted(group.members.items(), key=lambda pair: pair[0]):
        payoff_by_member_name[name] = []
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
            rk_class.payoff = class_payoff
            payoff_by_member_name[name] += [(alt, class_payoff) for alt in rk_class.alternatives]
            class_payoff += rk_class.frequency

    for alt in group.alternatives:
        alt_payoff_values = [
            [pair[1] for pair in payoff_by_member_name[member_name] if pair[0] is alt][0]
            for member_name in group.members
        ]
        payoff_global.append(
            [alt] + alt_payoff_values + [sum(alt_payoff_values)]
        )
    return sorted(payoff_global, key=lambda row: row[-1], reverse=True)
