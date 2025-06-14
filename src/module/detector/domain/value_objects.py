class Language:
    __slots__ = ('_part_one',)

    """
    Represents only the first set of ISO 639-1 codes.
    """
    _part_one: str

    def __init__(self, part_one: str):
        if len(part_one) != 2:
            raise ValueError("part_one must be a two-letter string")

        self._part_one = part_one

    def __str__(self) -> str:
        return self._part_one

    def __eq__(self, other):
        if not isinstance(other, Language):
            return NotImplemented
        return self._part_one == other._part_one

    @property
    def part_one(self) -> str:
        return self._part_one

    @classmethod
    def from_part_one(cls, part_one: str) -> 'Language':
        return cls(part_one=part_one)
