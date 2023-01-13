import boto3
import json
import os
from lambda_handlers.handlers import http_handler
from lambda_handlers.errors import InternalServerError
from cr_terrenos.response_formatter import ResponseFormatter

dynamo_db = boto3.resource(
    'dynamodb', region_name=str(os.getenv('REGION')))
db_table = str(os.getenv('DYNAMODB_TABLE'))

@http_handler()
def lambda_handler(event, context):
    if os.getenv("REGION", None) == None:
        raise InternalServerError("The region has not been configured")
    if os.getenv("DYNAMODB_TABLE", None) == None:
        raise InternalServerError("The dynamo database table has not been configured")
    table = dynamo_db.Table(db_table)
    response = table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return ResponseFormatter.format(data)
