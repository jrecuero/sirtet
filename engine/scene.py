from engine.nobject import NObject


class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.nobjects = []
        self.enable = True

    def update(self):
        pass

    def render(self):
        for obj in self.nobjects:
            obj.render(self.screen)

    def add_object(self, obj: NObject) -> bool:
        self.nobjects.append(obj)
        return True
