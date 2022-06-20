from datetime import date, datetime, timedelta
from urllib.parse import urljoin

import requests
from pynytimes import NYTAPI


def format_result(result):
    temp = {}
    for v in result[0]:
        temp.update({
            v['label'].lower(): v['score']
        })
    return temp


class NYTimesSentiment:

    def __init__(
        self,
        api_key: str,
        hf_inference_url: str = 'http://vpn.tchen.xyz:33960/',
    ):
        self.nyt = NYTAPI(api_key)
        self.url = urljoin(hf_inference_url, 'pipeline')

    def __call__(self, dt: datetime) -> dict:
        dt = date(dt.year, dt.month, dt.day) if not isinstance(dt, date) else dt
        articles = self.nyt.article_search(
            dates={
                # these are inclusive
                "begin": dt,
                "end": dt + timedelta(days=1) - timedelta(seconds=1.),
            },
            options={"sort": "relevance"}
        )
        payload = {
            'input': articles[0]['abstract'][:1000],
            'params': {
                'task': 'sentiment-analysis',
                'return_all_scores': True,
            }
        }
        result = requests.post(self.url, json=payload).json().get('result')
        return format_result(result) if result is not None else {}
