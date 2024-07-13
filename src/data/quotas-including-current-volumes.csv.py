import sys
import requests

response = requests.get(
    'https://data.api.trade.gov.uk/v1/datasets/uk-trade-quotas/versions/latest/reports/quotas-including-current-volumes/data',
    params={'format': 'csv'},
)
response.raise_for_status()
sys.stdout.buffer.write(response.content)
