from flask import Flask, request
from twilio import twiml
import random
import requests
import config #api keys and other sensitive data stored here

syn_url = 'https://api.syniverse.com/scg-external-api/api/v1/messaging/message_requests'
syn_headers = {'Authorization': 'Bearer ' + config.syn_access_token, 'Content-Type': 'application/json'}

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

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello from my Flask app!'

@app.route('/testroute', methods=['POST'])
def test_route():
    return 'you POSTed to /testroute'

@app.route('/testsms', methods=['POST'])
def test_sms():
    mobile_number = [config.my_mobile]
    payload = {"to":mobile_number,"body":"Someone just POSTed to /testroute","from":"sender_id:" + config.syn_sender_id}
    response = requests.post(syn_url, json=payload, headers=syn_headers)
    return 'test sms sent with status code '+str(response.status_code), 201

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
        event_data = json_data['event']
        mobile_number = [event_data['fld-val-list']['from_address']]
        payload = {"to":mobile_number,"body":eightball_response(),"from":"sender_id:" + config.syn_sender_id}
        response = requests.post(syn_url, json=payload, headers=syn_headers)
        return 'sms response sent with status code '+str(response.status_code), 201
    else:
        mobile_number = [config.my_mobile]
        payload = {"to":mobile_number,"body":"you POSTed without any JSON","from":"sender_id:" + config.syn_sender_id}
        response = requests.post(syn_url, json=payload, headers=syn_headers)
        return 'someone POSTed without any JSON to /eightball/syniverse', 201
