```py
import gzip
import json
import base64
import boto3

def lambda_handler(event, context):
    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    AWS_BUCKET_NAME = 'nginx-logs-store'
    s3 = boto3.resource('s3')
    data = payload
    object = s3.Object(AWS_BUCKET_NAME, 'results.json')
    object.put(
        Body=(bytes(json.dumps(payload).encode('UTF-8')))
    )

    log_events = payload['logEvents']
    for log_event in log_events:
        print(f'LogEvent: {log_event}')
```
