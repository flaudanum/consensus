import pytest

from consensus.entities.ranking_process import RankingProcess
from consensus.exceptions import PayoffError


@pytest.fixture(scope="function")
def rk_process():
    return RankingProcess()


def test_create_alternatives(rk_process):
    rk_process.new_alternative("Ulysses", "Leopold in Dublin")
    rk_process.new_alternative("Fahrenheit 451", "Guy is a fireman")

    assert rk_process.alternatives == {
        "Ulysses": {"description": "Leopold in Dublin"},
        "Fahrenheit 451": {"description": "Guy is a fireman"}
    }


def test_cannot_create_two_alternatives_with_same_name(rk_process):
    rk_process.new_alternative("Kid A", "Come on kids")

    for name in ("Kid A", "kid a", "KID A"):
        with pytest.raises(ValueError) as excinfo:
            rk_process.new_alternative(name, "This Kid shall not exist")

        excinfo.match(f"An alternative with name '{name}' already exists")


def test_create_members(rk_process):
    rk_process.new_member("Igor")
    rk_process.new_member("Grichka")

    assert rk_process.members == ["Grichka", "Igor"]


def test_cannot_create_two_members_with_same_name(rk_process):
    rk_process.new_member("Armelle")

    for name in ("Armelle", "armelle", "ARMELLE"):
        with pytest.raises(ValueError) as excinfo:
            rk_process.new_member(name)

        excinfo.match(f"A member with name '{name}' already exists")


@pytest.mark.parametrize('case', ['main success', 'incomplete ranking'])
def test_specify_member_ranking(rk_process, case):
    rk_process.new_member("Friedrich")

    assert rk_process.get_ranking("Friedrich") is None

    # Defines alternatives
    for name in ("A", "B", "C", "D", "E", "F", "G"):
        rk_process.new_alternative(name)

    ranking_list = [
        ["A", "C", "E"],
        ["B"],
        ["D", "F", "G"]
    ]

    rk_process.make_ranking(
        name="friedrich",
        ranking=ranking_list
    )

    assert rk_process.get_ranking("Friedrich") == [["A", "C", "E"], ["B"], ["D", "F", "G"]]


@pytest.mark.parametrize("case", ["no member", "one member"])
def test_computing_payoff_requires_at_least_two_members(rk_process, case):
    if case == "one member":
        rk_process.new_member("Member")

    with pytest.raises(PayoffError) as excinfo:
        rk_process.payoff()

    excinfo.match("Computing a payoff requires at least two members: ")


def test_computing_payoff_requires_that_alternatives_have_been_specified(rk_process):
    for name in ("A", "B", "C"):
        rk_process.new_member(f"Member {name}")

    with pytest.raises(PayoffError) as excinfo:
        rk_process.payoff()

    excinfo.match("Cannot compute a payoff as no alternatives are specified.")


def test_computing_payoff_requires_that_every_member_made_a_ranking(rk_process):
    for name in ("A", "B", "C"):
        rk_process.new_member(f"Member {name}")

    # Defines alternatives
    for name in ("A", "B", "C", "D", "E", "F", "G"):
        rk_process.new_alternative(name)

    rk_process.make_ranking(
        name="Member A",
        ranking=[
            ["A", "C", "E"],
            ["B"],
            ["D", "F", "G"]
        ]
    )

    with pytest.raises(PayoffError) as excinfo:
        rk_process.payoff()

    # Reports error for the first member without ranking in alphabetical order
    excinfo.match("Member 'Member B' must make a ranking.")
