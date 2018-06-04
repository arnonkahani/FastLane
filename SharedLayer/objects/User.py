from typing import List

from SharedLayer.objects.Analytics import Analytics


class User:
    def __init__(self, user_id: str = None, analytics: List[Analytics] = None):
        self.user_id = user_id
        self.analytics = analytics

    def to_dict(self):
        user_dict = {}
        user_dict['user_id'] = self.user_id
        user_dict['analytics'] = list(map(lambda event: event.to_dict(),self.analytics))
        return user_dict
