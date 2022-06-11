from datetime import datetime

from stpd.fourier import Fourier


def test_fourier():
    Fourier()(datetime(2020, 1, 1))
