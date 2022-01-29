import json
import boto3
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

ses_client = boto3.client('ses', region_name='ap-south-1')
client = boto3.client('logs')
CHARSET = "utf-8"
SENDER = 'saatwikmehta@gmail.com'
RECIPIENT = 'saatwikmehta@gmail.com'


def lambda_handler(event, context):
    get_log_group_response = client.describe_log_groups()['logGroups']
    get_log_group_name = [i['logGroupName'] for i in get_log_group_response]
    get_final_events = []
    date_24_hrs = datetime.today() - timedelta(hours=24)

    for group_name in get_log_group_name:
        get_stream_data = client.describe_log_streams(logGroupName=group_name,
                                                      logStreamNamePrefix=f"{date_24_hrs.strftime('%Y/%m/%d')}/")
        if get_stream_data['logStreams'] is not []:
            for i in get_stream_data['logStreams']:
                response = client.get_log_events(
                    logGroupName=group_name,
                    logStreamName=i['logStreamName'],
                    startFromHead=True
                )

                get_final_events.append({group_name: response['events']})

    msg = MIMEMultipart('mixed')

    msg['Subject'] = 'CloudWatchLogs24hrs'
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    att = MIMEApplication(bytes(json.dumps(get_final_events, indent=2, ensure_ascii=False).encode("utf-8")))
    att.add_header('Content-Disposition', 'attachment', filename="CloudWatchLogs24hrs.log")
    msg.attach(att)
    response = ses_client.send_raw_email(
        Source=SENDER,
        Destinations=[
            RECIPIENT
        ],
        RawMessage={
            'Data': msg.as_string(),
        }
    )
    # ses_client.send_email(Source='saatwikmehta@gmail.com',
    #                       Destination={
    #                           'ToAddresses': [
    #                               'saatwikmehta@gmail.com'
    #                           ]},
    #                       Message={
    #                           'Subject': {
    #                               'Data': 'CloudWatchLogs24hrs',

    #                           },
    #                           'Body': {
    #                               'Text': {
    #                                   'Data': json.dumps(get_final_events, indent=2, ensure_ascii=False),
    #                               },
    #                           }
    #                       }
    #                       )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
