from typing import List, Tuple
from datetime import datetime, date
from holidays import country_holidays


def get_pre_post_event_dates(event_dates: List[date], dt: date) -> Tuple[date, date]:
    pre_event_dt, post_event_dt = None, None
    for event_dt in sorted(event_dates):
        if event_dt <= dt:
            pre_event_dt = event_dt
        elif pre_event_dt is not None and event_dt > dt:
            post_event_dt = event_dt
            break
    return pre_event_dt, post_event_dt


class Holiday:
    def __init__(self, country: str = 'US'):
        self.country = country

    def __call__(self, dt: datetime) -> dict:
        dt = dt.date() if isinstance(dt, datetime) else dt
        us_holidays = country_holidays('US', years=[dt.year - 1, dt.year, dt.year + 1])
        pre_event_dt, post_event_dt = get_pre_post_event_dates(
            event_dates=list(us_holidays.keys()), dt=dt)
        return {
            f'{self.country.lower()}_holiday_days_since_last': (dt - pre_event_dt).days,
            f'{self.country.lower()}_holiday_days_to_next': (post_event_dt - dt).days,
        }
