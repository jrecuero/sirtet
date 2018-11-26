from engine.nobject import NObject


class Scene:
    def __init__(self):
        self.nobjects = []
        self.enable = True

    def update(self):
        pass

    def render(self, screen):
        for obj in self.nobjects:
            obj.render(screen)

    def add_object(self, obj: NObject) -> bool:
        self.nobjects.append(obj)
        return True
