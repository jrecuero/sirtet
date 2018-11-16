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
        self.skill: int = skill
        self.class_damage: int = 1
        self.class_life: int = 1
        self.class_skill: int = 1
