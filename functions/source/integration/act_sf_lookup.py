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
import logging

from salesforce import Salesforce
from act_util import get_arg

logger = logging.getLogger()

def lambda_handler(event, context):
  logger.info("event: %s" % json.dumps(event))

  sf = Salesforce(version=get_arg(os.environ, "SF_VERSION"), 
    consumer_key=get_arg(os.environ, "SF_CONSUMER_KEY"), 
    consumer_secret=get_arg(os.environ, "SF_CONSUMER_SECRET"), 
    username=get_arg(os.environ, "SF_USERNAME"), 
    password=get_arg(os.environ, "SF_PASSWORD") + get_arg(os.environ, "SF_ACCESS_TOKEN"))  
  if get_arg(os.environ, "SF_PRODUCTION").lower() == "true":
    sf.set_production()
  
  sf.sign_in()
  resp = lookup(sf=sf, **event['Details']['Parameters'])
  logger.info("result: %s" % resp)
  return resp

def lookup(sf, sf_object, sf_fields, **kwargs):
  where = " AND ".join([where_parser(*item) for item in kwargs.items()])
  query = "SELECT %s FROM %s WHERE %s" % (sf_fields, sf_object, where)
  records = sf.query(query=query)
  count = len(records)
  result = records[0] if count > 0 else {}
  result['sf_count'] = count
  return result
    
def where_parser(key, value):
  if key.lower() in ['mobilephone', 'homephone']:
    return "%s LIKE '%%%s%%%s%%%s%%'" % (key, value[-10:-7], value[-7:-4], value[-4:])
    
  if "%" in value:
    return "%s LIKE '%s'" % (key, value)

  return "%s='%s'" % (key, value)

