from consensus.entities.alternative import Alternative


def test_create_alternative():
    alternative = Alternative(
        name='Kid A',
        description="This is Kid A"
    )

    assert alternative.name == 'Kid A'
    assert alternative.description == 'This is Kid A'


def test_serialize():
    alternative = Alternative(
        name="Hailing to the thief",
        description="Smooth and dark"
    )

    assert alternative.serialize() == {
        "name": "Hailing to the thief",
        "description": "Smooth and dark"
    }


def test_load_from_serialization():
    serialization = {
        "name": "Hailing to the thief",
        "description": "Smooth and dark"
    }
    alternative = Alternative.load(serialization)

    assert alternative.name == "Hailing to the thief"
    assert alternative.description == "Smooth and dark"
