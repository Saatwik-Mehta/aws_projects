from pprint import pprint
import logging
from boto3 import client
from botocore import exceptions
logging.basicConfig(filename='create_s3_bucket.log',
                    level=logging.ERROR,
                    format='%(asctime)s: %(levelname)s:'
                           ' %(filename)s->'
                           ' %(funcName)s->'
                           ' Line %(lineno)d-> %(message)s')

def create_bucket(access_control_list, bucket_name, configure_bucket):
    try:
        s3_client = client('s3')
        bucket = s3_client.create_bucket(ACL=access_control_list,
                                         Bucket=bucket_name,
                                         CreateBucketConfiguration=configure_bucket)
        pprint(bucket)
    except exceptions.ClientError as client_err:
        logging.error("%s: %s",client_err.__class__.__name__, client_err)


if __name__ == '__main__':
    create_bucket(configure_bucket={'LocationConstraint': 'ap-south-1'},
                  bucket_name='my-1-sdk-bucket',
                  access_control_list='private')
