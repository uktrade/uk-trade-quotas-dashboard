import json
import sys
import requests

def get_version_ids():
    r = requests.get(
        'https://data.api.trade.gov.uk/v1/datasets/uk-trade-quotas/versions',
        params={'format': 'json'},
    )
    r.raise_for_status()
    return [
        version['id']
        for version in r.json()['versions']
        if version['id'] not in ('v1.0.5', 'v1.0.12', 'v1.0.14', 'v1.0.15', 'v1.0.18',)  # Data seems to be missing for these
    ]

def get_balances(version_id, quota_order_number):
    r = requests.get(
        f'https://data.api.trade.gov.uk/v1/datasets/uk-trade-quotas/versions/{version_id}/data',
        params={
            'format': 'json',
            'query-s3-select': f'''
                SELECT
                    q.quota_definition__initial_volume,
                    q.quota_definition__fill_rate,
                    q.quota_definition__balance,
                    q.quota_definition__last_allocation_date,
                    q.quota_definition__sid,
                    q.quota_definition__status
                FROM
                    S3Object[*].quotas[*] q
                WHERE
                    q.quota__order_number = '{quota_order_number}'
                    AND q.quota_definition__last_allocation_date IS NOT NULL
            ''',
        },
    )
    r.raise_for_status()
    return r.json()['rows']

data = [
    row
    for version_id in get_version_ids()
    for row in get_balances(version_id, quota_order_number='050097')
]

def days_since_2021(dateString):
    dateSlices = dateString.split('-')
    return ( ((int(dateSlices[0])-2021)*365)+((int(dateSlices[1])-0)*31)+int(dateSlices[2])-0 )

outs = []
for row in data:
    outs.append({'fill_rate':row['quota_definition__fill_rate'], 'days':days_since_2021(row['quota_definition__last_allocation_date'])})
sys.stdout.buffer.write(json.dumps(outs).encode('utf-8'))
