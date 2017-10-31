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
import wave, json, io, base64
import unittest

from google import cut_wav_at, Speech, __process_resp__, __create_req__

class Google_test(unittest.TestCase):

  def test_wav_cut_at_lower(self):
    with open("test/talk-to-aria-solutions.wav", "rb") as src:
      data = cut_wav_at(src, 1)
      with wave.open(data, "rb") as dst:
        self.assertEqual(1, dst.getnframes() / float(dst.getframerate()))

  def test_wav_cut_at_greater(self):
    with open("test/talk-to-aria-solutions.wav", "rb") as src:
      data = cut_wav_at(src, 60)
      with wave.open(data, "rb") as dst:
        self.assertAlmostEqual(1.619625, dst.getnframes() / float(dst.getframerate()), places=5)

  @unittest.skip("key required")
  def test_end_to_end(self):
    speech = Speech(key="TODO")
    with open("test/talk-to-aria-solutions.wav", "rb") as src:
      self.assertEqual("talk to Aria Solutions.", speech.recognize(src))
  
  def test_process_resp(self):
    resp_body = json.loads("""{
  "results": [
    {
      "alternatives": [
        {
          "transcript": "talk to Aria Solutions",
          "confidence": 0.8811072
        }
      ]
    }
  ]
}""")
    self.assertEqual("talk to Aria Solutions.", __process_resp__(resp_body))

  def test_process_resp_empty(self):
    self.assertEqual("", __process_resp__({}))

  def test_create_req(self):
    data = io.BytesIO("hello world".encode())

    req = __create_req__(data, "abc", "en-US")

    self.assertTrue("url" in req)
    self.assertTrue("?key=abc" in req["url"])
    self.assertTrue("data" in req)

    req_data = json.loads(req['data'])
    self.assertTrue("audio" in req_data)
    self.assertTrue("content" in req_data['audio'])
    self.assertEqual("hello world", base64.b64decode(req_data['audio']["content"]).decode())
    self.assertTrue("config" in req_data)
    self.assertTrue("languageCode" in req_data['config'])
    self.assertEqual("en-US", req_data['config']['languageCode'])
    