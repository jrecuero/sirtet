# damage: 4 life: 1 skill: 1 -> Berserker
# damage: 1 life: 4 skill: 1 -> Templar
# damage: 1 life: 1 skill: 4 -> Mage
# damage: 3 life: 2 skill: 1 -> Warrior
# damage: 3 life: 1 skill: 2 -> Hunter
# damage: 2 life: 3 skill: 1 -> Knight
# damage: 1 life: 3 skill: 2 -> Cleric
# damage: 2 life: 1 skill: 3 -> BattleMage
# damage: 1 life: 2 skill: 3 -> Alchemist
# damage: 2 life: 2 skill: 2 -> Rogue


class Job:
    def __init__(self):
        self.damage: int = 1
        self.life: int = 1
        self.skill: int = 1


class Berseker(Job):
    def __init__(self):
        super(Berseker, self).__init__()
        self.damage = 4
        self.life = 1
        self.skill = 1


class Templar(Job):
    def __init__(self):
        super(Templar, self).__init__()
        self.damage = 1
        self.life = 4
        self.skil = 1


class Mage(Job):
    def __init__(self):
        super(Mage, self).__init__()
        self.damage = 1
        self.life = 1
        self.skill = 4


class Warrior(Job):
    def __init__(self):
        super(Warrior, self).__init__()
        self.damage = 3
        self.life = 2
        self.skill = 1


class Hunter(Job):
    def __init__(self):
        super(Hunter, self).__init__()
        self.damage = 3
        self.life = 1
        self.skill = 2


class Knight(Job):
    def __init__(self):
        super(Knight, self).__init__()
        self.damage = 2
        self.life = 3
        self.skil = 1


class Cleric(Job):
    def __init__(self):
        super(Cleric, self).__init__()
        self.damage = 1
        self.life = 3
        self.skill = 2


class BattleMage(Job):
    def __init__(self):
        super(BattleMage, self).__init__()
        self.damage = 2
        self.life = 1
        self.skill = 3


class Alchemist(Job):
    def __init__(self):
        super(Alchemist, self).__init__()
        self.damage = 1
        self.life = 2
        self.skill = 3


class Rogue(Job):
    def __init__(self):
        super(Rogue, self).__init__()
        self.damage = 2
        self.life = 2
        self.skill = 2
