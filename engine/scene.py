from typing import List, Any
from engine.nobject import NObject
from engine.event import Event


class Scene:
    def __init__(self, name: str = ""):
        self.name: str = name
        self.nobjects: List[NObject] = []
        self.enable: bool = True

    def setup(self):
        pass

    def update(self, *events: Event):
        pass

    def render(self, screen: Any) -> List[Event]:
        events: List[Event] = []
        for obj in self.nobjects:
            events.extend(obj.render(screen))
        return events

    def add_object(self, obj: NObject) -> bool:
        self.nobjects.append(obj)
        return True

    def del_object(self, obj: NObject) -> bool:
        self.nobjects.remove(obj)
        return True
