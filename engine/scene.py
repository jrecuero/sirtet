from typing import List, Any
from engine.nobject import NObject
from engine.event import Event, Timer, EventTimer


def update(f):
    def _update(self: "Scene", *events: Event) -> List[Event]:
        if self.enable:
            new_events = list(events)
            for t in self.timers:
                if t.inc():
                    new_events.append(EventTimer(t))
            new_events.extend(self.update_objects(*new_events))
            return f(self, *new_events)
        return []

    return _update


def render(f):
    def _render(self: "Scene", screen: Any) -> List[Event]:
        if self.visible:
            new_events = self.render_objects(screen)
            new_events.extend(f(self, screen))
            return new_events
        return []

    return _render


class Scene:
    def __init__(self, name: str = ""):
        self.name: str = name
        self.nobjects: List[NObject] = []
        self.enable: bool = True
        self.visible: bool = True
        self.timers: List[Timer] = []

    def activate(self):
        self.enable = True
        self.visible = True

    def deactivate(self):
        self.enable = False
        self.visible = False

    def setup(self):
        pass

    def update_objects(self, *events: Event) -> List[Event]:
        new_events: List[Event] = []
        for obj in self.nobjects:
            new_events.extend(obj.update(*events))
        return new_events

    def render_objects(self, screen: Any) -> List[Event]:
        events: List[Event] = []
        for obj in self.nobjects:
            events.extend(obj.render(screen))
        return events

    @update
    def update(self, *events: Event) -> List[Event]:
        return list(events)

    @render
    def render(self, screen: Any) -> List[Event]:
        return []

    def add_object(self, obj: NObject) -> bool:
        self.nobjects.append(obj)
        return True

    def del_object(self, obj: NObject) -> bool:
        self.nobjects.remove(obj)
        return True

    def new_timer(self, timeout: int, enable: bool = True) -> Timer:
        t = Timer(timeout, enable)
        return self.add_timer(t)

    def add_timer(self, t: Timer) -> Timer:
        self.timers.append(t)
        return t

    def del_timer(self, t: Timer) -> None:
        self.timers.remove(t)
