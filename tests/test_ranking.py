from consensus.entities.alternative import Alternative
from consensus.entities.ranking import Ranking


def test_iter_over_ranking():
    alternatives = []

    # Defines alternatives
    for name in ('strawberries', 'blackberries', 'banana', 'pear'):
        alternatives.append(
            Alternative(
                name=name,
                description=f"Validation test 'main scenarion': alternative '{name}'"
            )
        )

    alt_name_ranking = [
        ['banana', ],
        ['blackberries', 'pear'],
        ['strawberries']
    ]

    ranking = Ranking(
        alternatives,
        sets=alt_name_ranking
    )

    assert alt_name_ranking == [[alt.name for alt in alt_sets] for alt_sets in ranking]
