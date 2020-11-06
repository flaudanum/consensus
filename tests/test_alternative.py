import pytest

from consensus.alternative import Alternative


def test_create_alternative():
    alternative = Alternative(
        name='Kid A',
        description="This is Kid A"
    )

    assert alternative.name == 'Kid A'
    assert alternative.description == 'This is Kid A'

    assert Alternative.get_names() == {'kid a'}
    del alternative


def test_cannot_create_two_alternatives_with_same_name():
    """
    Cannot creat two alternatives w/ the same name (not case sensitive)
    """
    # This object would be garbage cleaned w/o this dummy assignment
    _ = Alternative(
        name="Kid A",
        description="This is Kid A"
    )

    for name in ("Kid A", "kid a", "KID A"):
        with pytest.raises(ValueError) as excinfo:
            Alternative(
                name,
                description="This Kid A's clone shall not exist"
            )

        excinfo.match(f"An alternative with name '{name}' already exists")
