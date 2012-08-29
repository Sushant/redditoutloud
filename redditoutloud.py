"""
RedditOutLoud: A script that makes a call to the specified number and reads the
current top story on Reddit.

Sushant Bhadkamkar
mailsushant@gmail.com

"""

import urllib
import urllib2
import json
import time

from twilio.rest import TwilioRestClient

# Fill in appropriate values for the following
ACCOUNT_SID = 'TWILIOACCOUNTSID'
AUTH_TOKEN = 'TWILIOAUTHTOKEN'
MY_TWILIO_NUMBER = 'TWILIONUMBER'
NUMBER_TO_CALL = 'NUMBERTOCALL'

REDDIT_URL = 'http://www.reddit.com/top/.json'

# The audio message is generated using Twimlets
BASE_TWIML_URL = 'http://twimlets.com/message'


class RedditOutLoud:

  def __init__(self):
    self.client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    self.message = 'If you hear this message, an error occurred.'

  def get_top_story(self):
    while(True):
      try:
        json_response = urllib2.urlopen(REDDIT_URL)
        jd = json.JSONDecoder()
        response = jd.decode(json_response.read())
        top_story = response['data']['children'][3]['data']['title']
        # The extra periods are for introducing pauses
        self.message = 'Hi, this is RedditOutLoud. .'
        self.message += 'The top story on reddit right now is, '
        self.message += top_story + '. . '
        self.message += 'Goodbye, and have a great day!'
        return
      except Exception as fault:
        # On occasions, Reddit API returns an HTTP 429, wait and retry
        time.sleep(15)

  def make_call(self):
    self.get_top_story()
    # URL encode the message
    message_param = urllib.quote('Message[0]') + '=' + \
              urllib.quote(self.message)
    
    # The Twimlet URL generates a TWIML Response which will be converted to speech
    twiml_url = BASE_TWIML_URL + '?' + message_param
    call = self.client.calls.create(to=NUMBER_TO_CALL, from_=MY_TWILIO_NUMBER,
            url=twiml_url)


if __name__ == '__main__':
  reddit_out_loud = RedditOutLoud()
  reddit_out_loud.make_call()
