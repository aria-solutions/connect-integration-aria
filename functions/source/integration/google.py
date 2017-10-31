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
import io, wave, json, base64, logging
from botocore.vendored import requests

logger = logging.getLogger()

class Speech:

  def __init__(self, key, lang="en-US"):
    self.key = key
    self.lang = lang

  def recognize(self, data):
    data = cut_wav_at(data, 59)
    req = __create_req__(data, self.key, self.lang)
    logger.debug("google req: %s" % str(resp))
    resp = requests.post(**req).json()
    logger.debug("google resp: %s" % resp.text)
    return __process_resp__(resp)

def __create_req__(data, key, lang):
  content = base64.b64encode(data.read()).decode("utf-8")
  req_body = '{"audio": {"content": "%s"},"config": {"languageCode": "%s"}}' % (content, lang)
  url = 'https://speech.googleapis.com/v1/speech:recognize?key=%s' % key
  return {'url':url, 'data':req_body}

def __process_resp__(resp_body):
  """
  https://cloud.google.com/speech/reference/rest/v1/speech/recognize#response-body
  """
  if 'results' not in resp_body:
      logger.info("No result from Google")
      return ""

  sentences = [alternatives["transcript"] 
      for result in resp_body['results']
      for alternatives in result["alternatives"]]

  transcript = "%s." % ". ".join(sentences)
  logger.debug("google transcript: %s" % transcript)
  return transcript

def cut_wav_at(src_data, sec):
  with wave.open(src_data, 'rb') as src:
    dst_data = io.BytesIO()
    with wave.open(dst_data, 'wb') as dst:
      dst.setframerate(src.getframerate())
      dst.setsampwidth(2)
      dst.setnchannels(1)
      frames_to_write = min(src.getnframes(), sec * src.getframerate())
      dst.writeframes(src.readframes(frames_to_write))
      dst.close()
    dst_data.seek(0)
  return dst_data
    
