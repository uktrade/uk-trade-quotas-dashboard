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

def get_balances(version_id, quota_order_numbers):
    quota_order_numbers_sql = ','.join([f"'{order_number}'" for order_number in quota_order_numbers])

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
                    q.quota_definition__status,
                    q.quota_definition__validity_start_date,
                    q.quota__order_number
                FROM
                    S3Object[*].quotas[*] q
                WHERE
                    q.quota__order_number IN ({quota_order_numbers_sql})
                    AND q.quota_definition__last_allocation_date >= '2022-01-01'
            ''',
        },
    )
    r.raise_for_status()
    return r.json()['rows']

def remove_duplicates(l):
    return [dict(t) for t in {tuple(d.items()) for d in l}]

quota_order_numbers=['050097','050096','050120','050212','050035','050232']

data = remove_duplicates(
    row
    for version_id in get_version_ids()
    for row in get_balances(version_id, quota_order_numbers=quota_order_numbers)
)

outData={}
for orderNumber in quota_order_numbers:
    outData[orderNumber]=[]
    for row in data:
        if row['quota__order_number']==orderNumber:
            outData[orderNumber].append(row)
sys.stdout.buffer.write(json.dumps(outData).encode('utf-8'))
