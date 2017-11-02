"""
MIT License

Copyright 2017 Aria Solutions Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import cfnresponse
import traceback
from botocore.vendored import requests
import io, wave, base64

def handler(event, context):
  try:
    if event['RequestType'] == 'Create':
      production = event['ResourceProperties']['SF_PRODUCTION'].lower() == "true"
      consumer_key = event['ResourceProperties']['SF_CONSUMER_KEY']
      consumer_secret = event['ResourceProperties']['SF_CONSUMER_SECRET']
      username = event['ResourceProperties']['SF_USERNAME']
      password = event['ResourceProperties']['SF_PASSWORD'] + event['ResourceProperties']['SF_ACCESS_TOKEN']
      test_salesforce(production, consumer_key, consumer_secret, username, password)

      key = event['ResourceProperties']['GOOGLE_KEY']
      if key:
        test_google_speech(key)

    elif event['RequestType'] == 'Update':
      pass
    elif event['RequestType'] == 'Delete':
      pass
    cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, '')
  except:
    print(traceback.print_exc())
    cfnresponse.send(event, context, cfnresponse.FAILED, {}, '')

def test_salesforce(production, consumer_key, consumer_secret, username, password):
  print('Testing Salesforce crendentials')
  auth_data = {
    'grant_type': 'password',
    'client_id': consumer_key,
    'client_secret': consumer_secret,
    'username': username,
    'password': password
  }
  headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
  url = 'https://login.salesforce.com' if production else 'https://test.salesforce.com'
  resp = requests.post(url=url+"/services/oauth2/token", params=auth_data, headers=headers)
  
  if resp.status_code // 100 == 2:
    return

  data = resp.json()
  if 'error' in data:
    raise Exception("%s: %s" % (data['error'], data['error_description']))

  raise Exception("Error login into Salesforce")  

def test_google_speech(key):
  print("Testing Google Speech API")
  audio_raw = io.BytesIO()
  with wave.open(audio_raw, "w") as wav:
    wav.setframerate(16000)
    wav.setsampwidth(2)
    wav.setnchannels(1)
  audio_raw.seek(0)
  
  content = base64.b64encode(audio_raw.read()).decode()
  data = "{'audio': {'content': '%s'},'config': {'languageCode': 'en-US'}}" % content
  url = 'https://speech.googleapis.com/v1/speech:recognize?key=%s' % key
  resp = requests.post(url, data)

  if resp.status_code // 100 != 2:
    raise Exception("Error using Google Speech API")