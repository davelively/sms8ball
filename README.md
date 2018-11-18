# SMS Magic Eight Ball bot
This is an API written in Python 3.6 and uses the [Flask](http://flask.pocoo.org) microframework.

It will respond to incoming requests with a random response from the classic [Magic Eight Ball](https://en.wikipedia.org/wiki/Magic_8-Ball) fortune-telling toy.

This application supports incoming POST calls from either [Twilio](https://www.twilio.com) on the /eightball/twilio path or [Syniverse](https://developer.syniverse.com) on the /eightball/syniverse path

For Twilio, the response is sent back in the response to the incoming POST request using TwiML.

For Syniverse, the response is sent back using an API call to the Syniverse SMS API.  Creditials for that API are in a separate file called config.py, which is hidden from github using .gitignore.  For this code to work for you, you will need to create your own config.py file that looks like the following:
```python
syn_sender_id =    'your sender_id here'
syn_access_token = 'your access token here'
```
