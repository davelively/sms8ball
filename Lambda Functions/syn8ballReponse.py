import os
import random
from botocore.vendored import requests

def eightball_response():
    responses = [
        'As I see it, yes',
        'It is certain',
        'It is decidedly so',
        'Most likely',
        'Outlook good',
        'Signs point to yes',
        'Without a doubt',
        'Yes',
        'Yes - definitely',
        'You may rely on it',
        'Reply hazy, try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don’t count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful']
    return random.choice(responses)

def lambda_handler(event, context):
    #using environment variables to store the URL, access token, and sender id
    url = os.environ.get("syniverse_sms_url")
    headers = {'Authorization': 'Bearer ' + os.environ.get("syn_access_token"),
               'Content-Type': 'application/json'}

    #grab the phone number to respond to from the json in the incoming event 
    smsDestination = event["event"]["fld-val-list"]["from_address"]
    smsText = eightball_response()

    payload = {"to":[smsDestination],
               "body":smsText,
               "from":"sender_id:" + os.environ.get("syn_sender_id")}
    response = requests.post(url, json=payload, headers=headers)
    return 'Sent ', smsText, 'to ', smsDestination, response.status_code
