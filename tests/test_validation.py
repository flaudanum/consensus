import pandas as pd

from consensus.entities.ranking_process import RankingProcess


def test_main_scenario():
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
