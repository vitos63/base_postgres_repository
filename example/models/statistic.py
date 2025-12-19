from dataclasses import dataclass


@dataclass
class Statistic:
    total: int = 0
    monthly: int = 0
    weekly: int = 0
    daily: int = 0
    total_consultation: int = 0
    monthly_consultation: int = 0
    weekly_consultation: int = 0
    daily_consultation: int = 0
