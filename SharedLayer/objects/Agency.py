from typing import List

from SharedLayer.objects.Route import Route


class Agency:
    def __init__(self, id: str = None, name: str = None, url: str = None, routes: List[Route] = None):
        self.id = id
        self.name = name
        self.url = url
        self.routes = routes
