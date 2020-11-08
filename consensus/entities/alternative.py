class Alternative:

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    def __init__(self, name: str, description: str = ""):
        self._name = name
        self._description = description

    def serialize(self):
        return {
            "name": self._name,
            "description": self._description
        }

    @staticmethod
    def load(serialization: dict):
        return Alternative(
            name=serialization["name"],
            description=serialization["description"]
        )
