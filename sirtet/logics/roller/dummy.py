from sirtet.logics.roller.jobs import Job


class Dummy:
    def __init__(
        self,
        name: str,
        life: int,
        damage: int,
        skill: int,
        job: Job = Job(),
        player: bool = False,
    ):
        self.name: str = name
        self.description: str = ""
        self.damage: int = damage
        self.life: int = life
        self.__max_life: int = life
        self.skill: int = 0
        self.__max_skill: int = skill
        self.job = job
        self.__player: bool = player

    def get_damage(self, damage: int) -> int:
        return damage * self.job.damage * self.damage

    def get_life(self, life: int) -> int:
        return life * self.job.life

    def get_skill(self, skill: int) -> int:
        return skill * self.job.skill

    def damaged(self, damage: int) -> "Dummy":
        self.life -= damage
        return self

    def healed(self, heal: int) -> "Dummy":
        self.life += heal
        if self.life > self.__max_life:
            self.life = self.__max_life
        return self

    def skilled(self, skill: int) -> "Dummy":
        self.skill += skill
        if self.skill > self.__max_skill:
            self.skill = self.__max_skill
        return self

    def __str__(self) -> str:
        return "{:<8} [{}]\n{} {:>3}/{:<3} [{}]\n{} {:>3}/{:<3} [{}]\n{} {:>3}     [{}]".format(
            self.name,
            self.job.__class__.__name__,
            chr(9825),
            self.life,
            self.__max_life,
            self.job.life,
            chr(9733),
            self.skill,
            self.__max_skill,
            self.job.skill,
            chr(9784) if self.__player else chr(9763),
            self.damage,
            self.job.damage,
        )
