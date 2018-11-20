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
    def __init__(self, name: str, life: int, damage: int, skill: int):
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
        return "{0:<8} Life: {1:<4} Skil: {2:<4}".format(
            self.name, self.life, self.skill
        )
