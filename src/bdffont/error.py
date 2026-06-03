
class BdfError(Exception):
    pass


class BdfParseError(BdfError):
    pass


class BdfMissingWordError(BdfParseError):
    word: str

    def __init__(self, word: str):
        self.word = word

    def __str__(self) -> str:
        return f'missing word: {self.word!r}'


class BdfIllegalWordError(BdfParseError):
    word: str

    def __init__(self, word: str):
        self.word = word

    def __str__(self) -> str:
        return f'illegal word: {self.word!r}'


class BdfCountError(BdfParseError):
    word: str
    expected: int
    actual: int

    def __init__(self, word: str, expected: int, actual: int):
        self.word = word
        self.expected = expected
        self.actual = actual

    def __str__(self) -> str:
        return f'the count of {self.word!r} is incorrect: {self.expected} -> {self.actual}'


class BdfDumpError(BdfError):
    pass


class BdfXlfdError(BdfError):
    pass
