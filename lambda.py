#!/usr/bin/env python
# coding:utf-8
import boto3
import textwrap
import json
import re
from dateutil.parser import parse

#email config
region = ''
sendFrom = ''
sendTo = ''
subject = ""


def send_email(sendFrom, sendTo, subject, mailBody):
    client = boto3.client('ses', region_name=region)

    response = client.send_email(
        Source=sendFrom,
        Destination={
            'ToAddresses': [
                sendTo,
            ]
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': mailBody,
                },
            }
        }
    )

    return response

def make_body(message):
    mailBody = '''
    '''
    
    mailBody += message
    
    mailBody += '''
    '''
    
    return mailBody

def make_response(statusCode, message):
   return {
        'headers': {
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Headers ': '*'
        },
        'body': '{"message": "' + message + '"}',
        'code': statusCode,
    }
    
def validation(event):
    if "message" not in event:
        return make_response(500, 'error')
    return None

def lambda_handler(event, context):
    err = validation(event)
    if err:
        return err
        
    mailBody = make_body(event['message'])
    response = send_email(sendFrom, sendTo, subject, mailBody)
    return make_response(200, 'ok')

