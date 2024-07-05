import sys
import requests

sys.stdout.buffer.write(requests.get(
    'https://data.api.trade.gov.uk/v1/datasets/uk-trade-quotas/versions/latest/reports/quotas-including-current-volumes/data',
    params={'format': 'csv'},
).content)
