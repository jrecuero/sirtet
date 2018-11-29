from typing import Dict, List, Callable, Optional


class EVT:
    class ENG:
        KEY: int = 100
        TIMER: int = 200
        INPUT: int = 300

    class SCN:
        ISCENE: int = 400
        NEXT_SCENE: int = 401
        PREV_SCENE: int = 402
        FIRST_SCENE: int = 403
        LAST_SCENE: int = 404


class Timer:
    def __init__(self, timeout: int, enable: bool = True):
        self.timeout: int = timeout
        self.__counter: int = 0
        self.enable: bool = enable

    def inc(self) -> bool:
        if self.enable:
            self.__counter += 1
            if self.__counter >= self.timeout:
                self.__counter = 0
                return True
        return False


class Event:
    def __init__(self, evt: int, **kwargs):
        self.evt = evt
        self.params = kwargs

    def get_key(self) -> Optional[int]:
        if self.evt == EVT.ENG.KEY:
            return self.params.get("key", None)
        return None

    def get_timer(self) -> Optional[Timer]:
        if self.evt == EVT.ENG.TIMER:
            return self.params.get("timer", None)
        return None

    def get_input(self) -> Optional[str]:
        if self.evt == EVT.ENG.INPUT:
            return self.params.get("input_str", None)
        return None

    def get_iscene(self) -> Optional[int]:
        if self.evt == EVT.SCN.ISCENE:
            return self.params.get("iscene", None)
        return None

    def exit_on_key(self, key: str):
        if self.evt == EVT.ENG.KEY and self.get_key() == ord(key):
            exit(0)


class EventKey(Event):
    def __init__(self, key: int):
        super(EventKey, self).__init__(EVT.ENG.KEY, key=key)


class EventTimer(Event):
    def __init__(self, t: Timer):
        super(EventTimer, self).__init__(EVT.ENG.TIMER, timer=t)


class EventInput(Event):
    def __init__(self, data: str):
        super(EventInput, self).__init__(EVT.ENG.INPUT, input_str=data)


class EventIScene(Event):
    def __init__(self, iscene: int):
        super(EventIScene, self).__init__(EVT.SCN.ISCENE, iscene=iscene)


class EventNextScene(Event):
    def __init__(self):
        super(EventNextScene, self).__init__(EVT.SCN.NEXT_SCENE)


class EventPrevScene(Event):
    def __init__(self):
        super(EventPrevScene, self).__init__(EVT.SCN.PREV_SCENE)


class EventFirstScene(Event):
    def __init__(self):
        super(EventFirstScene, self).__init__(EVT.SCN.FIRST_SCENE)


class EventLastScene(Event):
    def __init__(self):
        super(EventLastScene, self).__init__(EVT.SCN.LAST_SCENE)


class KeyHandler:
    def __init__(self, keyreg: Dict[str, Callable[[], List[Event]]]):
        self.keyreg = keyreg

    def update(self, event: Event) -> List[Event]:
        event_to_return: List[Event] = []
        if event.evt == EVT.ENG.KEY and event.get_key() is not None:
            key = event.get_key()
            for k, cb in self.keyreg.items():
                if key == ord(k):
                    return cb()
        return event_to_return
