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
import unittest, unittest.mock

from act_sf_transcribe import create_case, update_task
class TranscribeTest(unittest.TestCase):

  def test_create_case(self):
    sf = unittest.mock.Mock()
    call_trace = {
      "ContactId": "abc",
      "CustomerEndpoint": {"Address": "abcd"},
      "Recording": {'Transcription':"hello world"},
      "Attributes":{}
    }

    create_case(sf, call_trace)

    _, kwargs = sf.create.call_args

    self.assertTrue("sobject" in kwargs)
    self.assertEqual("Case", kwargs['sobject'])
    self.assertTrue("data" in kwargs)
    data = kwargs['data']
    self.assertTrue("AC_Contact_Id__c" in data)
    self.assertEqual("abc", data['AC_Contact_Id__c'])
    self.assertTrue("SuppliedPhone" in data)
    self.assertEqual("abcd", data['SuppliedPhone'])
    self.assertTrue("Description" in data)
    self.assertEqual("hello world", data['Description'])
    self.assertTrue("Origin" in data)
    self.assertTrue("Status" in data)
    

  def test_update_task(self):
    sf = unittest.mock.Mock()
    call_trace = {
      "ConnectedToSystemTimestamp": "one",
      "DisconnectTimestamp": "two",
      "Queue": {
        "Duration": 11, 
        "Name": "my-name"
      },
      "Recording": {'Transcription':"hello world"}
    }

    update_task(sf, call_trace, "abc1")

    _, kwargs = sf.update.call_args

    self.assertTrue("sobject" in kwargs)
    self.assertEqual("Task", kwargs['sobject'])
    self.assertTrue("sobj_id" in kwargs)
    self.assertEqual("abc1", kwargs['sobj_id'])
    self.assertTrue('data' in kwargs)
    data = kwargs['data']
    self.assertTrue('Connected_To_System__c' in data)
    self.assertEqual("one", data['Connected_To_System__c'])
    self.assertTrue('Disconnected_From_System__c' in data)
    self.assertEqual("two", data['Disconnected_From_System__c'])
    self.assertTrue('Call_Transcript__c' in data)
    self.assertEqual("hello world", data['Call_Transcript__c'])
    self.assertTrue('QueueTime__c' in data)
    self.assertEqual(11, data['QueueTime__c'])
    self.assertTrue('Queue_Name__c' in data)
    self.assertEqual('my-name', data['Queue_Name__c'])

  def test_update_task_long_transcription(self):
    sf = unittest.mock.Mock()
    call_trace = {
      "ConnectedToSystemTimestamp": "",
      "DisconnectTimestamp": "",
      "Queue": {
        "Duration": 0, 
        "Name": ""
      },
      "Recording": {
        'Transcription':"A"*300
      }
    }

    update_task(sf, call_trace, "abc1")

    _, kwargs = sf.update.call_args    
    self.assertEqual(255, len(kwargs['data']['Call_Transcript__c']))

