import pandas as pd

from consensus.entities.alternative import Alternative
from consensus.entities.group import Group
from consensus.entities.member import Member
from consensus.payoff import payoff
from consensus.pd_payoff_table import pd_payoff_table


def test_main_scenario():
    alternatives = []

    # Defines alternatives
    alternative_names = {"Australia", "California US", "Costa Rica", "Germany", "Hungary", "Japan", "Thailand", "UK",
                         "Venezuela"}
    for name in alternative_names:
        alternatives.append(
            Alternative(
                name=name,
                description=f"Destination for holidays is {name}."
            )
        )

    # Creates a group of members which much rank alternatives
    group = Group(alternatives)

    # Adds members to the group
    group.new_member('Manon')
    group.new_member('Martin')

    assert Alternative.get_names() == set([name.lower() for name in alternative_names])
    assert Member.get_names() == {'manon', 'martin'}

    group.members['Manon'].make_ranking(
        alternatives,
        ranking=[
            ["Thailand", "Venezuela"],
            ["Australia", "Costa Rica"],
            ["Hungary"],
            ["California US", "Germany", "UK"],
            ["Japan"]
        ]
    )

    group.members['Martin'].make_ranking(
        alternatives,
        ranking=[
            ["Japan", "Germany", "Hungary"],
            ["Australia", "California US"],
            ["UK", "Thailand", "Venezuela", "Costa Rica"]
        ]
    )

    payoff_values = payoff(group)

    reference = pd.DataFrame.from_dict({
        'Hungary': {'Manon': 0.4444444444444444, 'Martin': 0.6666666666666666, 'payoff': 1.1111111111111112},
        'Australia': {'Manon': 0.5555555555555556, 'Martin': 0.4444444444444444, 'payoff': 1.0},
        'Thailand': {'Manon': 0.7777777777777778, 'Martin': 0.0, 'payoff': 0.7777777777777778},
        'Venezuela': {'Manon': 0.7777777777777778, 'Martin': 0.0, 'payoff': 0.7777777777777778},
        'Germany': {'Manon': 0.1111111111111111, 'Martin': 0.6666666666666666, 'payoff': 0.7777777777777777},
        'Japan': {'Manon': 0.0, 'Martin': 0.6666666666666666, 'payoff': 0.6666666666666666},
        'California US': {'Manon': 0.1111111111111111, 'Martin': 0.4444444444444444,
                          'payoff': 0.5555555555555556},
        'Costa Rica': {'Manon': 0.5555555555555556, 'Martin': 0.0, 'payoff': 0.5555555555555556},
        'UK': {'Manon': 0.1111111111111111, 'Martin': 0.0, 'payoff': 0.1111111111111111}
    }, orient="index")

    pd.testing.assert_frame_equal(
        reference,
        pd_payoff_table(payoff_values, group),
    )
