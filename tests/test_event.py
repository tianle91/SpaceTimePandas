from stpd.event import Holiday
import datetime


def test_holiday():
    Holiday('US')(datetime.date(2022, 1, 17))
