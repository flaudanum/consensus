from consensus.alternative import Alternative
from consensus.group import Group


def test_create_group_and_add_member():
    alternatives = []

    # Defines alternatives
    for name in ('A', 'B', 'C', 'D'):
        alternatives.append(
            Alternative(
                name=name,
                description=f"Unit test create_group_and_add_member"
            )
        )

    group = Group(alternatives)

    group.new_member('Marie')
    group.new_member('Pierre')

    assert group.members['Marie'].name == 'Marie'
    assert group.members['Pierre'].name == 'Pierre'

    assert sorted([alt.name for alt in group.alternatives]) == ['A', 'B', 'C', 'D']
    assert group.num_alternatives == 4
