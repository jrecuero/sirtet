from typing import Optional

EVT_ENG_KEY: int = 100
EVT_ENG_TIMER: int = 200
EVT_ENG_INPUT: int = 300
EVT_SCN_ISCENE: int = 400
EVT_SCN_NEXT_SCENE: int = 401
EVT_SCN_PREV_SCENE: int = 402
EVT_SCN_FIRST_SCENE: int = 403
EVT_SCN_LAST_SCENE: int = 404


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
        if self.evt == EVT_ENG_KEY:
            return self.params.get("key", None)
        return None

    def get_timer(self) -> Optional[Timer]:
        if self.evt == EVT_ENG_TIMER:
            return self.params.get("timer", None)
        return None

    def get_input(self) -> Optional[str]:
        if self.evt == EVT_ENG_INPUT:
            return self.params.get("input_str", None)
        return None

    def get_iscene(self) -> Optional[int]:
        if self.evt == EVT_SCN_ISCENE:
            return self.params.get("iscene", None)
        return None


class EventKey(Event):
    def __init__(self, key: int):
        super(EventKey, self).__init__(EVT_ENG_KEY, key=key)


class EventTimer(Event):
    def __init__(self, t: Timer):
        super(EventTimer, self).__init__(EVT_ENG_TIMER, timer=t)


class EventInput(Event):
    def __init__(self, data: str):
        super(EventInput, self).__init__(EVT_ENG_INPUT, input_str=data)


class EventIScene(Event):
    def __init__(self, iscene: int):
        super(EventIScene, self).__init__(EVT_SCN_ISCENE, iscene=iscene)


class EventNextScene(Event):
    def __init__(self):
        super(EventNextScene, self).__init__(EVT_SCN_NEXT_SCENE)


class EventPrevScene(Event):
    def __init__(self):
        super(EventPrevScene, self).__init__(EVT_SCN_PREV_SCENE)


class EventFirstScene(Event):
    def __init__(self):
        super(EventFirstScene, self).__init__(EVT_SCN_FIRST_SCENE)


class EventLastScene(Event):
    def __init__(self):
        super(EventLastScene, self).__init__(EVT_SCN_LAST_SCENE)
