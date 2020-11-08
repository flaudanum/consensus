from consensus.entities.alternative import Alternative
from consensus.entities.member import Member
from consensus.entities.ranking import Ranking


def test_create_alternative():
    member = Member(name='Friedrich')

    assert member.name == 'Friedrich'


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
