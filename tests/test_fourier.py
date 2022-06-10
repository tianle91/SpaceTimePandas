from stpd.fourier import Fourier
from datetime import datetime


def test_fourier():
    Fourier()(datetime(2020, 1, 1))
