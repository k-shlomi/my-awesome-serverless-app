import json

import boto3

USERS_TABLE = "Users"
dynamodb_client = boto3.client(
    'dynamodb', region_name='us-east-1', endpoint_url='http://localstack:4566'
)


def _verify_response(response):
    if "Error" in response:
        print(response)
        raise Exception(f"HTTPStatusCode: {response['ResponseMetadata']['HTTPStatusCode']}"
                        f"message={response['Error']['Message']}")


def get_user(event, context):
    user_id = event['pathParameters']["user_id"]
    result = dynamodb_client.get_item(
        TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
    )
    _verify_response(result)
    item = result.get('Item')

    if not item:
        return {"statusCode": 404, "body": json.dumps({})}
    body = {'user_id': item.get('userId').get('S'), 'name': item.get('name').get('S')}
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response


def create_user(event, context):
    print(f"{event=}")
    request = json.loads(event["body"])
    user_id = request["user_id"]
    user_name = request["user_name"]
    result = dynamodb_client.put_item(
        TableName=USERS_TABLE, Item={'userId': {'S': user_id}, 'name': {'S': user_name}}
    )
    _verify_response(result)

    body = {
        "message": "Successfuly added a new user!"
    }
    response = {"statusCode": 201, "body": json.dumps(body)}
    return response
