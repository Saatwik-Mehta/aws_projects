"""
This module will give you the
list of IAM members of groups in your aws account
"""
from pprint import pprint
from boto3 import client


def get_group_members():
    """This function will return the List of dictionaries
     that contains the group name and IAM members inside
        a particular aws account.
    :return: List of dictionaries containing the group name and members
    """
    iam_client = client('iam')
    groups = iam_client.list_groups()
    group_names = [group['GroupName'] for group in groups['Groups']]
    return list({grp: [users['UserName']
                       for users in iam_client.get_group(GroupName=grp)['Users']]}
                for grp in group_names)


if __name__ == '__main__':
    pprint(get_group_members())
