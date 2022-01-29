import json
import logging
from boto3 import client
from botocore import exceptions

logging.basicConfig(filename='read_write_s3.log',
                    level=logging.ERROR,
                    format='%(asctime)s: %(levelname)s:'
                           ' %(filename)s->'
                           ' Line %(lineno)d-> %(message)s')

try:
    # -------------- get buckets----------------
    s3_client = client('s3')
    print("Buckets present:")
    for i, bucket in enumerate(s3_client.list_buckets()['Buckets']):
        print(i + 1, "-", bucket['Name'])
    # --------------- end ----------------------

    command = "y"
    while command == "y":

        # -------------- get objects in the bucket --------------
        bucket_name = input("Enter the name of the bucket:")
        response = s3_client.list_objects(Bucket=bucket_name)
        print("Objects present:")
        for i, filename in enumerate(response['Contents']):
            print(i + 1, " ", filename['Key'])
        # --------------- end ----------------------

        operation = input("Enter the operation number:"
                          "\n1->Upload a file"
                          "\n2->Delete the file"
                          "\n3->Read from the file\n:")

        if operation == '2':

            # ---------------- delete the file ----------------
            file_name = input("Enter the name of the file to delete:")
            response = s3_client.delete_object(Bucket=bucket_name,
                                               Key=file_name)

            print(f"{file_name} Successfully deleted")
            # --------------------- end ---------------------

        elif operation == '1':
            # ---------------- Upload a file ----------------
            file_name = input("Enter the name of the file to upload:")
            with open(file_name, 'rb') as file_to_upload_data:
                file_data = file_to_upload_data
                response = s3_client.put_object(Bucket=bucket_name,
                                                Body=file_data,
                                                Key=file_name)
            print(f"{file_name} Successfully uploaded")
            # --------------------- end ---------------------

        else:
            # ---------------- read from the file ----------------
            file_name = input("Enter the name of the file to read:")
            response = s3_client.get_object(Bucket=bucket_name,
                                            Key=file_name)
            print(response['Body'].read().decode("utf-8"))
            # --------------------- end ---------------------
        command = input("Do you want to perform operation again[y/n]:")

except exceptions.ClientError as client_error:
    logging.error("%s: %s", client_error.__class__.__name__, client_error)
except FileNotFoundError as file_error:
    logging.error("%s: %s", file_error.__class__.__name__, file_error)
except exceptions.NoCredentialsError as no_credentials_error:
    logging.error("%s: %s", no_credentials_error.__class__.__name__, no_credentials_error)
