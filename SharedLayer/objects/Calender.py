from typing import List


class Calender:
    def __init__(self, days: List[bool] = None, start_date: str = None, end_date: str = None):
        self.days = days
        self.start_date = start_date
        self.end_date = end_date
