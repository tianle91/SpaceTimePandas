import datetime

from stpd.event import Holiday


def test_holiday():
    Holiday(years=[2021, 2022, 2023], country='US')(datetime.date(2022, 1, 17))
