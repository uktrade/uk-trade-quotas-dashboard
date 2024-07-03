import json
import sys
import requests

r = requests.get(
    'https://data.api.trade.gov.uk/v1/datasets/uk-trade-quotas/versions',
    params={'format': 'json'},
)
r.raise_for_status()
r = requests.get(
    'https://data.api.trade.gov.uk/v1/datasets/uk-trade-quotas/versions/v1.0.491/data',
    params={
        'format': 'json',
        'query-s3-select': '''
            SELECT
                q.quota_definition__balance,
                q.quota_definition__last_allocation_date,
                q.quota_definition__sid,
                q.quota_definition__status
            FROM
                S3Object[*].quotas[*] q
            WHERE
                q.quota__order_number = '050006'
        ''',
    },
)
r.raise_for_status()

sys.stdout.buffer.write(json.dumps(r.json()['rows']).encode('utf-8'))
