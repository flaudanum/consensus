import pytest

from consensus.entities.alternative import Alternative
from consensus.entities.ranking import Ranking, Preference


def test_create_ranking_with_leveled_preferences():
    alternatives = []

    # Defines alternatives
    for name in ('Chess', 'Go', 'Backgammon', 'Checkers', 'Xiangqi', 'Shōgi', 'Oware'):
        alternatives.append(Alternative(name))

    alt_name_ranking = [
        ['Go', ],
        ['Chess', 'Xiangqi', 'Shōgi'],
        ['Checkers'],
        ['Backgammon', 'Oware']
     ]

    ranking = Ranking(alternatives, sets=alt_name_ranking)

    assert ranking.sets == [
        ['Go', ],
        ['Chess', 'Xiangqi', 'Shōgi'],
        ['Checkers'],
        ['Backgammon', 'Oware']
     ]

    assert ranking.intensities == {}

def test_iter_over_ranking():
    alternatives = []

    # Defines alternatives
    for name in ('strawberries', 'blackberries', 'banana', 'pear'):
        alternatives.append(
            Alternative(
                name=name,
                description=f"Validation test 'main scenario': alternative '{name}'"
            )
        )

    alt_name_ranking = [
        ['banana', ],
        ['blackberries', 'pear'],
        ['strawberries']
    ]

    ranking = Ranking(alternatives, sets=alt_name_ranking)

    assert alt_name_ranking == [[alt.name for alt in alt_sets] for alt_sets in ranking]


def test_create_ranking_with_variable_preference_intensities():
    alternatives = []

    # Defines alternatives
    for name in ('strawberries', 'blackberries', 'banana', 'pear'):
        alternatives.append(
            Alternative(
                name=name,
                description=f"Validation test 'main scenario': alternative '{name}'"
            )
        )

    # The number of intensities must equal the number of classes ('sets' argument) minus 1
    with pytest.raises(ValueError) as excinfo:
        Ranking(
            alternatives,
            sets=[
                ['banana', ],
                ['blackberries', 'pear'],
                ['strawberries']
            ],
            intensities=[
                Preference.VERY_STRONG,
            ]
        )
    excinfo.match("Expected number of intensity specifications is 2, provided: 1")

    ranking = Ranking(
        alternatives,
        sets=[
            ['banana', ],
            ['blackberries', 'pear'],
            ['strawberries']
        ],
        intensities=[
            Preference.VERY_STRONG,
            Preference.MODERATE
        ]
    )

    assert ranking.intensities == {
        (1,2): Preference.VERY_STRONG,
        (2,3): Preference.MODERATE,
    }
