import sys
import requests

r = requests.get(
    'https://data.api.trade.gov.uk/v1/datasets/uk-trade-quotas/versions',
    params={'format': 'json'},
)
sys.stdout.buffer.write(r.content)
