import boto3

s3_client = boto3.client('s3')


def get_s3_objects(bucket_name, get_file_path):
    response = s3_client.get_object(Bucket=bucket_name,
                                    Key=get_file_path)
    content = response['Body']
    file_content = content.read().decode("utf-8")
    return file_content


def delete_s3_objects(bucket_name, get_file_path):
    response = s3_client.delete_object(Bucket=bucket_name,
                                       Key=get_file_path)
    return f"{get_file_path} is deleted successfully"


def put_s3_objects(bucket_name, content, get_file_path):
    response = s3_client.put_object(Bucket=bucket_name,
                                    Key=get_file_path,
                                    Body=content)
    return f"{get_file_path} is uploaded successfully"
