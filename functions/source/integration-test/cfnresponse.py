#  Copyright 2016 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
#  This file is licensed to you under the AWS Customer Agreement (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at http://aws.amazon.com/agreement/ .
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied.
#  See the License for the specific language governing permissions and limitations under the License.
from __future__ import print_function
from botocore.vendored import requests

import sys
import traceback
import json

SUCCESS = "SUCCESS"
FAILED = "FAILED"

def send(event, context, responseStatus, responseData, physicalResourceId, reason=None):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = reason if reason else 'See the details in CloudWatch Log Stream: %s' % context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['Data'] = responseData if responseData else {}

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

class cfnresponse(object):
    def __init__(self, resource_id=None):
        self.resource_id = resource_id

    def __call__(self, fn):
        def wrapper(event, context):
            data = None
            msg = 'See the details in CloudWatch Log Stream: https://console.aws.amazon.com/cloudwatch/home?#logEventViewer:group=%s;stream=%s' % (context.log_group_name, context.log_stream_name)
            
            try:
                data = fn(event, context)
                status = SUCCESS
            except:
                traceback.print_exc()
                msg = '%s. %s' % (sys.exc_info()[1], msg)
                status = FAILED

            send(event, context, status, data, self.resource_id, msg)
            return data
        return wrapper