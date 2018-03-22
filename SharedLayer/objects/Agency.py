from typing import List

from SharedLayer.objects.Route import Route


class Agency:
    def __init__(self, id: str, name: str, url: str, routes: List[Route]):
        self.id = id
        self.name = name
        self.url = url
        self.routes = routes
