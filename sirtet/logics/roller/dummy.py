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


class Dummy:
    def __init__(
        self, name: str, life: int, damage: int, skill: int, player: bool = False
    ):
        self.name: str = name
        self.description: str = ""
        self.damage: int = damage
        self.life: int = life
        self.__max_life: int = life
        self.skill: int = 0
        self.__max_skill: int = skill
        self.class_damage: int = 1
        self.class_life: int = 1
        self.class_skill: int = 1
        self.__player: bool = player

    def get_damage(self, damage: int) -> int:
        return damage * self.class_damage * self.damage

    def get_life(self, life: int) -> int:
        return life * self.class_life

    def get_skill(self, skill: int) -> int:
        return skill * self.class_skill

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
        return "{:<8}\n{} {:>3}/{:<3} [{}]\n{} {:>3}/{:<3} [{}]\n{} {:>3}     [{}]".format(
            self.name,
            chr(9825),
            self.life,
            self.__max_life,
            self.class_life,
            chr(9733),
            self.skill,
            self.__max_skill,
            self.class_skill,
            chr(9784) if self.__player else chr(9763),
            self.damage,
            self.class_damage,
        )
