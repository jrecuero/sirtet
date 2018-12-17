class Spore:
    def __init__(self):
        self._dn: int = -1

    def equal(self, other: "Spore") -> bool:
        return self._dn == other._dn

    def match(self) -> bool:
        return True

    def __str__(self) -> str:
        return "_"

    def to_string(self) -> str:
        return self.__class__.__name__

    def render(self) -> None:
        pass


class Null(Spore):
    def __init__(self):
        super(Null, self).__init__()
        self._dn: int = 0

    def match(self) -> bool:
        return False

    def __str__(self) -> str:
        return "0"


class Damage(Spore):
    def __init__(self):
        super(Damage, self).__init__()
        self._dn: int = 1

    def __str__(self) -> str:
        # return "1"
        # return "{}".format(chr(9852))
        # return "{0}".format(chr(9770))
        return "{0}".format(chr(9784))


class Life(Spore):
    def __init__(self):
        super(Life, self).__init__()
        self._dn: int = 2

    def __str__(self) -> str:
        # return "2"
        return "{}".format(chr(9825))


class Skill(Spore):
    def __init__(self):
        super(Skill, self).__init__()
        self._dn: int = 3

    def __str__(self) -> str:
        # return "3"
        # return "{}".format(chr(9827))
        return "{}".format(chr(9733))


class Outch(Spore):
    def __init__(self):
        super(Outch, self).__init__()
        self._dn: int = 4

    def __str__(self) -> str:
        # return "4"
        # return "{}".format(chr(9819))
        return "{}".format(chr(9763))
