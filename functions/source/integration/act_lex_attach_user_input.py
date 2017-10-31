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
import json, logging

logger = logging.getLogger()

def lambda_handler(event, context):
  logger.info("event: %s" % json.dumps(event))
  resp = attach_user_input(event)
  logger.info("result: %s" % resp)
  return resp

def attach_user_input(event):
  session = {}
  if 'sessionAttributes' in event:
    session = event['sessionAttributes']
    
  user_input = []
  if 'user_input' in session:
    user_input = json.loads(session['user_input'])
    
  user_input.append(event['inputTranscript'])
  session['user_input'] = json.dumps(user_input)
    
  return {
    "sessionAttributes": session,
    "dialogAction": {
      "type": "Delegate",
      "slots": event['currentIntent']['slots']
    }   
  }