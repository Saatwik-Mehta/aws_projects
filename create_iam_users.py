"""
This module can be used to create a IAM user
for aws access and project contributions
"""
import getpass
import logging
import boto3
from botocore import exceptions


logging.basicConfig(filename='create_iam_users.log',
                    level=logging.ERROR,
                    format='%(asctime)s: %(levelname)s:'
                           ' %(filename)s->'
                           ' %(funcName)s->'
                           ' Line %(lineno)d-> %(message)s')


def create_users(user_name, password_reset_required=False):
    """
    Function to create IAM user with login profile
    :param user_name: Name of the IAM user that will be used for login purpose as well
    :param password_reset_required: If True, the created user will have
                                    to change the password on login
    :return: None
    """
    try:
        iam_client = boto3.client('iam')
        iam_client.create_user(UserName=user_name)

        password = getpass.getpass(f"Enter password for {user_name}: ")
        iam_client.create_login_profile(UserName=user_name,
                                        Password=password,
                                        PasswordResetRequired=password_reset_required)
        print("User login-profile created successfully")
    except exceptions.ClientError as client_err:
        logging.error('%s: %s', client_err.response['Error']['Code'],
                      client_err.response['Error']['Message'])
    except exceptions.ParamValidationError as valid_err:
        logging.error('%s: %s', valid_err.__class__.__name__,
                      valid_err)


if __name__ == '__main__':
    create_users(user_name='Abhila', password_reset_required=False)
