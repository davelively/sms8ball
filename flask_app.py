from flask import Flask, request
from twilio import twiml
import random
import requests
import config #api keys and other sensitive data stored here

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

def send_sms_syniverse(sender_id, to_number, body_text):
    url = 'https://api.syniverse.com/scg-external-api/api/v1/messaging/message_requests'
    headers = {'Authorization': 'Bearer ' + config.syn_access_token, 'Content-Type': 'application/json'}
    payload = {"to":[to_number],"body":body_text,"from":"sender_id:" + sender_id}
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello from my Flask app!'

@app.route('/testroute', methods=['POST'])
def test_route():
    return 'you POSTed to /testroute'

@app.route('/testsms', methods=['POST'])
def test_sms():
    response_status = send_sms_syniverse(config.syn_sender_id, config.my_mobile, "Someone just POSTed to /testroute")
    return 'test sms sent with status code '+str(response_status), 201

@app.route('/smstest/twilio', methods=['POST'])
def smstest_twilio():
    number = request.form['From']
    message_body = request.form['Body']

    resp = twiml.Response()
    resp.message('Hello from pythonanywhere {}, you asked: {}'.format(number, message_body))
    return str(resp)

@app.route('/smsfallback/twilio', methods=['POST'])
def smsfallback_twilio():
    resp = twiml.Response()
    resp.message("I didn't quite catch that - can you repeat your question?")
    return str(resp)

@app.route('/eightball/twilio', methods=['POST'])
def eightball_twilio():
    resp = twiml.Response()
    resp.message(eightball_response())
    return str(resp)

@app.route('/eightball/syniverse', methods=['POST'])
def eightball_syniverse():
    json_data = request.get_json()
    if json_data: #skip if no JSON - Python will raise an exception in the following code otherwise
        mobile_number = json_data['event']['fld-val-list']['from_address']
        response_text = eightball_response()
        response_status = send_sms_syniverse(config.syn_sender_id, mobile_number, response_text)
        return 'sms response sent with status code '+str(response_status), 201
    else:
        response_status = send_sms_syniverse(config.syn_sender_id, config.my_mobile, "you POSTed without any JSON")
        return 'someone POSTed without any JSON to /eightball/syniverse', 201
