import random
import json

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

# log the event to CloudWatch
print('Loading function')

def lambda_handler(event, context):
    # log the event to CloudWatch
    print("Received event: " + json.dumps(event, indent=2))

    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>' + eightball_response() + '</Message></Response>'
