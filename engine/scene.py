from typing import List, Any
from engine.nobject import NObject


class Scene:
    def __init__(self, name: str = ""):
        self.name: str = name
        self.nobjects: List[NObject] = []
        self.enable: bool = True

    def setup(self):
        pass

    def update(self, *events):
        pass

    def render(self, screen: Any) -> None:
        for obj in self.nobjects:
            obj.render(screen)

    def add_object(self, obj: NObject) -> bool:
        self.nobjects.append(obj)
        return True

    def del_object(self, obj: NObject) -> bool:
        self.nobjects.remove(obj)
        return True
