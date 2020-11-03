from consensus.alternative import Alternative
from consensus.group import Group
from consensus.member import Member
from consensus.payoff import payoff


def test_main_scenario():
    alternatives = []

    # Defines alternatives
    for name in ('A', 'B', 'C', 'D', 'E', 'F', 'G'):
        alternatives.append(
            Alternative(
                name=name,
                description=f"Validation test 'main scenarion': alternative '{name}'"
            )
        )

    # Creates a group of members which much rank alternatives
    group = Group(alternatives)

    # Adds members to the group
    group.new_member('Marie')
    group.new_member('Pierre')

    assert Alternative.get_names() == {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    assert Member.get_names() == {'marie', 'pierre'}

    group.members['Marie'].make_ranking(
        alternatives,
        ranking=[
            ['G', ],
            ['A', 'B'],
            ['C', 'E', 'F'],
            ['D']
        ]
    )

    group.members['Pierre'].make_ranking(
        alternatives,
        ranking=[
            ['A', 'C', 'E'],
            ['B'],
            ['D', 'F', 'G']
        ]
    )

    payoff_values = payoff(group)
    print(payoff_values)
