from consensus.entities.alternative import Alternative
from consensus.entities.member import Member


class Group:

    @property
    def members(self) -> dict[str, Member]:
        return {member.name: member for member in self._members}

    @property
    def alternatives(self):
        return self._alternatives

    @property
    def num_alternatives(self):
        return len(self._alternatives)

    def __init__(self, alternatives: list[Alternative]):
        self._members: list[Member] = []
        self._alternatives = alternatives

    def new_member(self, name) -> None:
        self._members.append(Member(name))
