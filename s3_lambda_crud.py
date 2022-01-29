import json
from s3_lambda_crud_methods import get_s3_objects,\
    delete_s3_objects, put_s3_objects


get_method = "GET"
delete_method = "DELETE"
put_method = "PUT"


def lambda_handler(event, context):
    bucket_name = event['bucket']
    get_http_method = event['httpMethod']
    get_file_path = event['path']
    if get_http_method == get_method:
        file_content = get_s3_objects(bucket_name, get_file_path)
    if get_http_method == delete_method:
        file_content = delete_s3_objects(bucket_name, get_file_path)
    if get_http_method == put_method:
        file_content = put_s3_objects(bucket_name, get_file_path, content=event['body'])
    if ".json" in get_file_path:
        return {
            'statusCode': 200,
            'body': json.loads(file_content)
        }
    return {
        'statusCode': 200,
        'body': file_content.encode("utf-8")
    }
