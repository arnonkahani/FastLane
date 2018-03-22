from typing import List


class Calender:
    def __init__(self, days: List[bool], start_date: str, end_date: str):
        self.days = days
        self.start_date = start_date
        self.end_date = end_date
