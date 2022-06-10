from datetime import datetime

from dataclasses import dataclass
from typing import Callable, Dict

from math import cos, sin, pi, ceil


@dataclass
class Period:
    conversion_fn: Callable[[datetime], float]
    period: float


PERIODS: Dict[str, Period] = {
    'week_of_year': Period(lambda dt: dt.isocalendar()[1], period=52.286),
    'day_of_month': Period(lambda dt: dt.day, period=30.437),
    'day_of_week': Period(lambda dt: dt.weekday(), period=7.),
    'hour_of_day': Period(lambda dt: dt.hour, period=24),
    'minute_of_hour': Period(lambda dt: dt.minute, period=60),
}

REGULARITY = {
    'sine': sin,
    'cos': cos,
}


class Fourier:

    def __init__(
        self,
        week_of_year: bool = True,
        day_of_month: bool = True,
        day_of_week: bool = True,
        hour_of_day: bool = True,
        minute_of_hour: bool = True,
        use_period_fraction: float = 1.,
    ):
        self.selected_periods = {}
        if week_of_year:
            self.selected_periods['week_of_year'] = PERIODS['week_of_year']
        if day_of_month:
            self.selected_periods['day_of_month'] = PERIODS['day_of_month']
        if day_of_week:
            self.selected_periods['day_of_week'] = PERIODS['day_of_week']
        if hour_of_day:
            self.selected_periods['hour_of_day'] = PERIODS['hour_of_day']
        if minute_of_hour:
            self.selected_periods['minute_of_hour'] = PERIODS['minute_of_hour']
        self.use_period_fraction = use_period_fraction

    def __call__(self, dt: datetime) -> dict:
        out = {}
        for period_name, period in self.selected_periods.items():
            for reg_name, reg_fn in REGULARITY.items():
                for i in range(ceil(period.period * self.use_period_fraction)):
                    out[f'{period_name}_{reg_name}_phase_{i}'] = reg_fn(
                        2 * pi * (period.conversion_fn(dt) + i) / period.period
                    )
        return out
