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
import datetime, os, json, io, csv, urllib.parse, logging
import boto3, botocore, botocore.stub

from salesforce import Salesforce

logger = logging.getLogger()

s3 = boto3.client("s3")
def lambda_handler(event, context):
  logger.info("event: %s" % json.dumps(event))

  event_record = event['Records'][0]
  bucket = event_record['s3']['bucket']['name']
  logger.debug("bucket: %s" % bucket)
  key = urllib.parse.unquote(event_record['s3']['object']['key'])
  logger.debug("key: %s" % key)
  data = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode()

  sf = Salesforce(version=get_arg(os.environ, "SF_VERSION"), 
    consumer_key=get_arg(os.environ, "SF_CONSUMER_KEY"), 
    consumer_secret=get_arg(os.environ, "SF_CONSUMER_SECRET"), 
    username=get_arg(os.environ, "SF_USERNAME"), 
    password=get_arg(os.environ, "SF_PASSWORD") + get_arg(os.environ, "SF_ACCESS_TOKEN"))  
  if get_arg(os.environ, "SF_PRODUCTION").lower() == "true":
    sf.set_production()
  sf.sign_in()

  for record in csv.DictReader(data.split("\n")):
    sf.create("ACT_HistoricalReportData__c", prepare_queue_record(record, event_record['eventTime'])) 
  logger.info("done")

def prepare_queue_record(record_raw, current_date): 
  record = {label_parser(k):value_parser(v) for k, v in record_raw.items()}
  record['type__c'] = "Queue" 
  record['created_date__c'] = current_date
  record['report_id__c'] = "%s%s" % (record['ac_object_name__c'], current_date)
  return record

def label_parser(key):
  if key.lower() == 'average agent interaction and customer hold time':
    return 'avg_agent_interaction_and_cust_hold_time__c'

  if key.lower() == "queue":
    return "ac_object_name__c"

  return "%s__c" % key.replace(" ", "_").lower() 

def value_parser(value):
  return value.replace("%", "") if len(value) > 0 else None

if __name__ == '__main__':
  import sf_config #set enviroment variables
  s3 = botocore.session.get_session().create_client('s3')
  stubber = botocore.stub.Stubber(s3)
  stubber.activate()
  bucket = "connect_bucket"
  key = "reports/interval-queue.csv"
  stream = open(key, 'r')#set Key to csv
  req = {"Bucket":bucket, 'Key':key}
  resp = {'Body': stream}
  stubber.add_response('get_object', resp, req)

  event = {'Records':[{
    's3':{"bucket":{"name":bucket}, "object":{"key":key}},
    'eventTime':"2017-10-03T22:00:51.444Z"
  }]}

  lambda_handler(event, None)
  stream.close()
  stubber.deactivate()

