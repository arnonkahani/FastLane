from shapely.geometry import Point


class Stop:
    def __init__(self, id: str, code: str, name: str, description: str, location: Point):
        self.id = id
        self.code = code
        self.name = name
        self.description = description
        self.location = location
