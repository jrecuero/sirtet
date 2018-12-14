from sirtet.logics.roller.jobs import Job


class Level:
    def __init__(self):
        self.xp: int = 0
        self.level: int = 1
        self.next: int = 1

    def set_next(self):
        self.next *= 2

    def add_xp(self, xp: int = 1) -> bool:
        self.xp += xp
        while self.xp >= self.next:
            self.level += 1
            self.set_next()
        return True


class Point(Level):
    def __init__(self):
        super(Point, self).__init__()

    def add_xp(self, xp: int = 1) -> bool:
        if xp > self.xp + self.next:
            return False
        return super(Point, self).add_xp(xp)


class Stat:
    def __init__(self, name: str, maxi: int, init: int = -1, own: int = -1):
        self.name: str = name
        self.val: int = init if init != -1 else maxi
        self.max: int = maxi
        self.own: int = own if own != -1 else maxi
        self.points: Point = Point()


class Dummy:
    def __init__(
        self,
        name: str,
        life: int,
        damage: int,
        skill: int,
        job: Job = Job(),
        is_player: bool = False,
    ):
        self.name: str = name
        self.description: str = ""
        self.damage: Stat = Stat("damage", damage)
        self.life: Stat = Stat("life", life, 0)
        self.skill: Stat = Stat("skill", skill, 0)
        self.defense: Stat = Stat("defense", 0)
        self.job = job
        self.is_player: bool = is_player
        self.level: Level = Level()

    def get_damage(self, damage: int) -> int:
        return damage * self.job.damage * self.damage.val

    def get_life(self, life: int) -> int:
        return life * self.job.life

    def get_skill(self, skill: int) -> int:
        return skill * self.job.skill

    def damaged(self, damage: int) -> "Dummy":
        self.life.val -= damage
        return self

    def healed(self, heal: int) -> "Dummy":
        self.life.val += heal
        if self.life.val > self.life.max:
            self.life.val = self.life.max
        return self

    def skilled(self, skill: int) -> "Dummy":
        self.skill.val += skill
        if self.skill.val > self.skill.max:
            self.skill.val = self.skill.max
        return self

    def __str__(self) -> str:
        return "{:<8} [{}]\n{} {:>3}/{:<3} [{}]\n{} {:>3}/{:<3} [{}]\n{} {:>3}     [{}]".format(
            self.name,
            self.job.__class__.__name__,
            chr(9825),
            self.life.val,
            self.life.max,
            self.job.life,
            chr(9733),
            self.skill.val,
            self.skill.max,
            self.job.skill,
            chr(9784) if self.is_player else chr(9763),
            self.damage.val,
            self.job.damage,
        )
