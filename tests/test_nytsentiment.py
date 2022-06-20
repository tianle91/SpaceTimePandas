from datetime import date

from stpd.nytsentiment import NYTimesSentiment
import os


def test_NYTimesSentiment():
    nytsentiment = NYTimesSentiment(api_key=os.getenv('NYT_API_KEY'))
    assert len(nytsentiment(date(2022, 6, 1))) == 2
