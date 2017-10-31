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
import unittest
from main import test_salesforce, test_google_speech

class CloudFormationTest(unittest.TestCase):

    def test_salesforce_sandbox_fail(self):
    SF_CONSUMER_KEY = "abc"
    SF_CONSUMER_SECRET = "abc"
    SF_USERNAME = "abc"
    SF_PASSWORD = "abc"
    SF_PRODUCTION = False

    with self.assertRaises(Exception):
      test_salesforce(SF_PRODUCTION,
        SF_CONSUMER_KEY, 
        SF_CONSUMER_SECRET,
        SF_USERNAME,
        SF_PASSWORD)

  @unittest.skip("Need Prod crendentials")
  def test_salesforce_production_success(self):
    SF_CONSUMER_KEY = ""
    SF_CONSUMER_SECRET = ""
    SF_USERNAME = ""
    SF_PASSWORD = ""
    SF_PRODUCTION = True

    test_salesforce(SF_PRODUCTION,
      SF_CONSUMER_KEY, 
      SF_CONSUMER_SECRET,
      SF_USERNAME,
      SF_PASSWORD)

  @unittest.skip("Need Sandbox crendentials")
  def test_salesforce_sandbox_success(self):
    SF_CONSUMER_KEY = ""
    SF_CONSUMER_SECRET = ""
    SF_USERNAME = ""
    SF_PASSWORD = ""
    SF_PRODUCTION = False

    test_salesforce(SF_PRODUCTION,
      SF_CONSUMER_KEY, 
      SF_CONSUMER_SECRET,
      SF_USERNAME,
      SF_PASSWORD)

  @unittest.skip("Need Google Key crendentials")  
  def test_google_speech_api_success(self):
    test_google_speech(key="")

  def test_google_speech_api_fail(self):
    with self.assertRaises(Exception):
      test_google_speech(key="abc")      