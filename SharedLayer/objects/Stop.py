from shapely.geometry import Point


class Stop:
    def __init__(self, id: str = None, code: str = None, name: str = None, description: str = None,
                 location: Point = None):
        self.id = id
        self.code = code
        self.name = name
        self.description = description
        self.location = location
