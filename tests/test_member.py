import pytest

from consensus.entities.alternative import Alternative
from consensus.entities.member import Member
from consensus.entities.ranking import Ranking


def test_create_alternative():
    member = Member(name='Friedrich')

    assert member.name == 'Friedrich'
    assert Member.get_names() == {'friedrich'}


def test_cannot_create_two_alternatives_with_same_name():
    """
    Cannot creat two members w/ the same name (not case sensitive)
    """
    # This object would be garbage cleaned w/o this dummy assignment
    _ = Member("Friedrich")

    for name in ("Friedrich", "friedrich", "FRIEDRICH"):
        with pytest.raises(ValueError) as excinfo:
            Member(name)
        excinfo.match(f"A member with name '{name}' already exists")

    del _


def test_specify_ranking():
    member = Member(name='Friedrich')
    alternatives = []

    # Defines alternatives
    for name in ('A', 'B', 'C', 'D', 'E', 'F', 'G'):
        alternatives.append(Alternative(name=name))

    member.make_ranking(
        alternatives,
        ranking=[
            ['A', 'C', 'E'],
            ['B'],
            ['D', 'F', 'G']
        ]
    )
    assert isinstance(member.ranking, Ranking)

    assert str(member.ranking) == "(('A', 'C', 'E'), ('B',), ('D', 'F', 'G'))"
