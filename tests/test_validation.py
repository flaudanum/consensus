from math import exp, log
import pandas as pd

from consensus.entities.ranking_process import RankingProcess
from consensus.entities.ranking import Preference


def test_base_method_main_scenario():
    # -------------------- R A N K I N G   P R O C E S S --------------------

    rk_process = RankingProcess()

    # Defines alternatives
    alternative_names = {"Australia", "California US", "Costa Rica", "Germany", "Hungary", "Japan", "Thailand", "UK",
                         "Venezuela"}
    for name in alternative_names:
        rk_process.new_alternative(
            name=name,
            description=f"Destination for holidays is {name}."
        )

    # Adds members to the group
    rk_process.new_member("Manon")
    rk_process.new_member("Martin")

    rk_process.make_ranking("manon", [
        ["Thailand", "Venezuela"],
        ["Australia", "Costa Rica"],
        ["Hungary"],
        ["California US", "Germany", "UK"],
        ["Japan"]
    ])

    rk_process.make_ranking("martin", [
        ["Japan", "Germany", "Hungary"],
        ["Australia", "California US"],
        ["UK", "Thailand", "Venezuela", "Costa Rica"]
    ])

    payoff_table = rk_process.payoff()

    # -------------------- A S S E R T I O N S --------------------

    assert rk_process.alternatives == {
        name: {"description": f"Destination for holidays is {name}."}
        for name in alternative_names
    }

    assert rk_process.members == ['Manon', 'Martin']

    assert rk_process.get_ranking("manon") == [
        ["Thailand", "Venezuela"],
        ["Australia", "Costa Rica"],
        ["Hungary"],
        ["California US", "Germany", "UK"],
        ["Japan"]
    ]

    assert rk_process.get_ranking("martin") == [
        ["Japan", "Germany", "Hungary"],
        ["Australia", "California US"],
        ["UK", "Thailand", "Venezuela", "Costa Rica"]
    ]

    reference = pd.DataFrame.from_dict({
        "Hungary": {"Manon": 0.4444444444444444, "Martin": 0.6666666666666666, "total": 1.1111111111111112},
        "Australia": {"Manon": 0.5555555555555556, "Martin": 0.4444444444444444, "total": 1.0},
        "Thailand": {"Manon": 0.7777777777777778, "Martin": 0.0, "total": 0.7777777777777778},
        "Venezuela": {"Manon": 0.7777777777777778, "Martin": 0.0, "total": 0.7777777777777778},
        "Germany": {"Manon": 0.1111111111111111, "Martin": 0.6666666666666666, "total": 0.7777777777777777},
        "Japan": {"Manon": 0.0, "Martin": 0.6666666666666666, "total": 0.6666666666666666},
        "California US": {"Manon": 0.1111111111111111, "Martin": 0.4444444444444444,
                          "total": 0.5555555555555556},
        "Costa Rica": {"Manon": 0.5555555555555556, "Martin": 0.0, "total": 0.5555555555555556},
        "UK": {"Manon": 0.1111111111111111, "Martin": 0.0, "total": 0.1111111111111111}
    }, orient="index")

    pd.testing.assert_frame_equal(reference, payoff_table)


def test_method_with_comparison_intensity():
    # -------------------- R A N K I N G   P R O C E S S --------------------

    rk_process = RankingProcess()

    # Defines alternatives
    alternative_names = ("A", "B", "C", "D", "E", "F", "G", "H")
    for name in alternative_names:
        rk_process.new_alternative(
            name=name,
            description=f"Alternative '{name}'"
        )

    # Adds members to the group
    rk_process.new_member("Grace")
    rk_process.new_member("Barbara")

    rk_process.make_ranking("Grace", [
        ["A", "B"],
        ["C", "D", "E"],
        ["F"],
        ["G", "H"]
    ])

    rk_process.make_ranking(
        "Barbara",
        [
            ["A", "B"],
            ["C", "D", "E"],
            ["F"],
            ["G", "H"]
        ],
        [
            Preference.VERY_STRONG,
            Preference.MODERATE,
            Preference.STRONG
        ]
    )

    payoff_table = rk_process.payoff()

    # -------------------- A S S E R T I O N S --------------------

    assert rk_process.get_ranking("Grace") == [
        ["A", "B"],
        ["C", "D", "E"],
        ["F"],
        ["G", "H"]
    ]
    assert rk_process.get_ranking("Barbara") == [
        ["A", "B"],
        ["C", "D", "E"],
        ["F"],
        ["G", "H"]
    ]

    # Reference values for Barbara's comparisons with variable intensities
    scaling = 1 + (exp(1 / 3 * log(10)) - 1) * 1 / 4 + (exp(1 / 3 * log(10) * 2) - 1) * 3 / 8
    c1_pf = (3 / 8 + 1 / 8 + 1 / 4 + (exp(1 / 3 * log(10) * 2) - 1) * 3 / 8 + (
                exp(1 / 3 * log(10)) - 1) * 1 / 4) / scaling
    c2_pf = (1 / 8 + 1 / 4 + (exp(1 / 3 * log(10)) - 1) * 1 / 4) / scaling
    c3_pf = (1 / 4 + (exp(1 / 3 * log(10)) - 1) * 1 / 4) / scaling

    reference = pd.DataFrame.from_dict({
        "A": {"Grace": 0.75, "Barbara": c1_pf, "total": 0.75 + c1_pf},
        "B": {"Grace": 0.75, "Barbara": c1_pf, "total": 0.75 + c1_pf},
        "C": {"Grace": 0.375, "Barbara": c2_pf, "total": 0.375 + c2_pf},
        "D": {"Grace": 0.375, "Barbara": c2_pf, "total": 0.375 + c2_pf},
        "E": {"Grace": 0.375, "Barbara": c2_pf, "total": 0.375 + c2_pf},
        "F": {"Grace": 0.25, "Barbara": c3_pf, "total": 0.25 + c3_pf},
        "G": {"Grace": 0, "Barbara": 0, "total": 0},
        "H": {"Grace": 0, "Barbara": 0, "total": 0},
    }, orient="index")

    pd.testing.assert_frame_equal(reference, payoff_table)
