class Spore:
    def __init__(self):
        pass

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

    def match(self) -> bool:
        return False

    def __str__(self) -> str:
        return "0"


class Damage(Spore):
    def __init__(self):
        super(Damage, self).__init__()

    def __str__(self) -> str:
        return "1"


class Life(Spore):
    def __init__(self):
        super(Life, self).__init__()

    def __str__(self) -> str:
        return "2"


class Skill(Spore):
    def __init__(self):
        super(Skill, self).__init__()

    def __str__(self) -> str:
        return "3"


class Outch(Spore):
    def __init__(self):
        super(Outch, self).__init__()

    def __str__(self) -> str:
        return "4"
