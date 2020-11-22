class RankedClass:
    __slots__ = ("frequency", "rank", "alternatives")

    def __repr__(self):
        return "{" + f"'frequency': {self.frequency}, 'rank': {self.rank}" + "}"
