from copy import deepcopy


class Alternative:
    __names = set()

    @staticmethod
    def get_names():
        return deepcopy(Alternative.__names)

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
        # Checks if the name is already used
        if name.lower() in Alternative.__names:
            raise ValueError(f"An alternative with name '{name}' already exists")
        else:
            Alternative.__names.add(name.lower())
        self._name = name
        self._description = description

    def __del__(self):
        if hasattr(self, '_name'):
            Alternative.__names.remove(self._name.lower())
