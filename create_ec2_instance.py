from boto3 import resource


def create_instance():
    ec2_resource = resource('ec2')

    ec2_instance = ec2_resource.create_instances(ImageId='ami-052cef05d01020f1d', InstanceType='t2.micro',
                                                 KeyName='MyEc2KeyPair', MaxCount=1, MinCount=1,
                                                 SecurityGroupIds=['sg-08d1f282f37ade5a1'],
                                                 SubnetId='subnet-0de27ce0bf523951a')


if __name__ == '__main__':
    create_instance()
