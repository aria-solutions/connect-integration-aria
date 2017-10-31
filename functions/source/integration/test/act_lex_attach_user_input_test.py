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
import unittest, json

from act_lex_attach_user_input import attach_user_input

class LexAttachUserInputTest(unittest.TestCase):

  def test_response_new(self):
    event = {
      'inputTranscript': "hello world",
      'currentIntent': {'slots':{'name':'alonso'}}
    }

    resp = attach_user_input(event)

    self.assertTrue('dialogAction' in resp)
    self.assertTrue('type' in resp['dialogAction'])
    self.assertEqual("delegate", resp['dialogAction']['type'].lower())
    self.assertTrue('slots' in resp['dialogAction'])
    self.assertEqual(event['currentIntent']['slots'], resp['dialogAction']['slots'])
    self.assertTrue("sessionAttributes" in resp)
    self.assertTrue("user_input" in resp["sessionAttributes"])
    user_inputs = json.loads(resp["sessionAttributes"]['user_input'])
    self.assertEqual(1, len(user_inputs))
    self.assertEqual("hello world", user_inputs[0])



  def test_response_subsequent(self):
    event = {
      'inputTranscript': "last",
      'currentIntent': {'slots':{}},
      'sessionAttributes': {'user_input':'["hello", "world"]'}
    }

    resp = attach_user_input(event)

    self.assertTrue("sessionAttributes" in resp)
    self.assertTrue("user_input" in resp["sessionAttributes"])
    user_inputs = json.loads(resp["sessionAttributes"]['user_input'])
    self.assertEqual(3, len(user_inputs))
    self.assertEqual("last", user_inputs[-1])
