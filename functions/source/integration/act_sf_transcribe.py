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
import json, os, urllib.parse, logging, traceback
from act_util import get_arg, split_bucket_key
import boto3
from botocore.client import Config
from salesforce import Salesforce
from google import Speech

logger = logging.getLogger()

s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

def lambda_handler(event, context):
  logger.info("event: %s" % json.dumps(event))

  event_record = event['Records'][0]
  bucket = event_record['s3']['bucket']['name']
  logger.debug("bucket: %s" % bucket)
  key = urllib.parse.unquote(event_record['s3']['object']['key'])
  logger.debug("key: %s" % key)

  call_traces_raw = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode()
  
  sf = Salesforce(version=get_arg(os.environ, "SF_VERSION"), 
    consumer_key=get_arg(os.environ, "SF_CONSUMER_KEY"), 
    consumer_secret=get_arg(os.environ, "SF_CONSUMER_SECRET"), 
    username=get_arg(os.environ, "SF_USERNAME"), 
    password=get_arg(os.environ, "SF_PASSWORD") + get_arg(os.environ, "SF_ACCESS_TOKEN"))  
  if get_arg(os.environ, "SF_PRODUCTION").lower() == "true":
    sf.set_production()
  
  sf.sign_in()

  for call_trace_raw in call_traces_raw.split("\n"):
    logger.debug("call trace: %s" % call_trace_raw)
    if len(call_trace_raw) == 0:
      continue

    call_trace = json.loads(call_trace_raw)
    for func in [process_transcribe, process_task_update]:
      try:
        func(sf, call_trace)  
      except Exception as ex:
        logger.error(traceback.print_exc())

  s3.delete_object(Bucket=bucket, Key=key)
  logger.info("done")

def process_task_update(sf, call_trace):
  logger.debug("process_transcribe: ")
  records = sf.query("SELECT Id FROM Task WHERE CallObject ='%s'" % call_trace['ContactId'])
  if len(records) != 1:
    logger.error("couldn't find only one Task for CallObject :'%s'" % call_trace['ContactId'])
    return

  task_id = records[0]['Id']
  update_task(sf, call_trace, task_id)

def process_transcribe(sf, call_trace):
  logger.debug("process_transcribe: ")

  if 'transcription' not in call_trace['Attributes'] or not call_trace['Attributes']['transcription']:
    logger.info("transcription disabled, set Attributes.transcription=true")
    return

  if not call_trace['Recording']:
    logger.info("Recording not present, enable recording on the call flow")
    return 

  rec_bucket, rec_key = split_bucket_key(call_trace['Recording']['Location'])
  logger.debug("recording bucket: %s" % rec_bucket)
  logger.debug("recording key: %s" % rec_key)

  audio = s3.get_object(Bucket=rec_bucket, Key=rec_key)['Body']
  
  speech = Speech(key=get_arg(os.environ, "GOOGLE_KEY"))
  transcription = speech.recognize(audio)
  call_trace['Recording']['Transcription'] = transcription

  if 'voicemail' not in call_trace['Attributes'] or not call_trace['Attributes']['voicemail']:
    logger.info("voicemail Case creating disabled, set Attributes.voicemail=true")
    return

  create_case(sf, call_trace)

def create_case(sf, call_trace):
  case = {}
  case['Origin'] = "Phone"
  case['Status'] = "New"
  case['Subject'] = "Voicemail"
  case['Description'] = call_trace['Recording']['Transcription']
  case['AC_Contact_Id__c'] = call_trace['ContactId']
  case['SuppliedPhone'] = call_trace["CustomerEndpoint"]["Address"]
  if 'sf_account_id' in call_trace['Attributes']:
    case['AccountId'] = call_trace['Attributes']['sf_account_id']
  if 'sf_contact_id' in call_trace['Attributes']:
    case['ContactId'] = call_trace['Attributes']['sf_contact_id']

  sf.create(sobject="Case", data=case)


def update_task(sf, call_trace, task_id):
  task = {}
  task['Connected_To_System__c'] = call_trace['ConnectedToSystemTimestamp']
  task['Disconnected_From_System__c'] = call_trace['DisconnectTimestamp']
  if 'Recording' in call_trace and 'Transcription' in call_trace['Recording']:
    transcription = call_trace['Recording']['Transcription']
    task['Call_Transcript__c'] = transcription[:min(len(transcription), 255)]

  if "Queue" in call_trace and call_trace['Queue']:
    task['QueueTime__c'] = call_trace['Queue']['Duration']
    task['Queue_Name__c'] = call_trace['Queue']['Name']

  sf.update(sobject="Task",sobj_id=task_id, data=task)