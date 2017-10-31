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
from botocore.vendored import requests

logger = logging.getLogger()

class Salesforce:

  def __init__(self, version, consumer_key, consumer_secret, username, password):
    self.request = Request()
    self.access_token = None
    self.host = None
    self.login_host = 'https://test.salesforce.com'
    self.version = version
    self.auth_data = {
      'grant_type': 'password',
      'client_id': consumer_key,
      'client_secret': consumer_secret,
      'username': username,
      'password': password
    }

  def set_production(self):
    self.login_host = 'https://login.salesforce.com'

  def sign_in(self):
    logger.debug("Salesforce: Sign in")
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    resp = self.request.post(url=self.login_host+"/services/oauth2/token", params=self.auth_data, headers=headers)
    data = resp.json()
    self.access_token = data['access_token']
    self.host = data['instance_url']
    self.headers = { 
      'Authorization': 'Bearer %s' % self.access_token,
      'Content-Type': 'application/json'
    }

  def search(self, query):
    logger.debug("Salesforce: Search")
    url = '%s/services/data/%s/search' % (self.host, self.version)
    resp = self.request.get(url=url, params={'q':query}, headers=self.headers)
    return resp.json()['searchRecords']

  def query(self, query):#TODO: create generator that takes care of subsequent request for more than 200 records
    logger.debug("Salesforce: Query")
    url = '%s/services/data/%s/query' % (self.host, self.version)
    resp = self.request.get(url=url, params={'q':query}, headers=self.headers)
    data = resp.json()
    for record in data['records']:
        del record['attributes']
    return data['records']

  def update(self, sobject, sobj_id, data):
    logger.debug("Salesforce: Update")
    url = '%s/services/data/%s/sobjects/%s/%s' % (self.host, self.version, sobject, sobj_id)
    self.request.patch(url=url, data=data, headers=self.headers)

  def update_by_external(self, sobject, field, sobj_id, data):
    logger.debug("Salesforce: Update by external")
    url = '%s/services/data/%s/sobjects/%s/%s/%s' % (self.host, self.version, sobject, field, sobj_id)
    self.request.patch(url=url, data=data, headers=self.headers)

  def create(self, sobject, data):
    logger.debug("Salesforce: Create")
    url = '%s/services/data/%s/sobjects/%s' % (self.host, self.version, sobject)
    resp = self.request.post(url=url, data=data, headers=self.headers)
    return resp.json()['id']

  def delete(self, sobject, sobject_id):
    logger.debug("Salesforce: Delete")
    url = '%s/services/data/%s/sobjects/%s/%s' % (self.host, self.version, sobject, sobject_id)
    resp = self.request.delete(url=url, headers=self.headers)

  def is_authenticated(self):
    return self.access_token and self.host

class Request:
  def post(self, url, headers, data=None, params=None):
    logger.debug("POST Requests:\nurl=%s\ndata=%s\nparams=%s" % (url, data, params))
    r = requests.post(url=url, data=json.dumps(data), params=params, headers=headers)
    logger.debug("Response: %s" % r.text)
    return __check_resp__(r)

  def delete(self, url, headers):
    logger.debug("DELETE Requests:\nurl=%s" % url)
    r = requests.delete(url=url, headers=headers)
    logger.debug("Response: %s" % r.text)
    return __check_resp__(r)

  def patch(self, url, data, headers):
    logger.debug("PATCH Requests:\nurl=%s\ndata=%s" % (url, data))
    r = requests.patch(url=url, data=json.dumps(data), headers=headers)
    logger.debug("Response: %s" % r.text)
    return __check_resp__(r)

  def get(self, url, params, headers):
    logger.debug("GET Requests:\nurl=%s\nparams=%s" % (url, params))
    r = requests.get(url=url, params=params, headers=headers)
    logger.debug("Response: %s" % r.text)
    return __check_resp__(r)

def __check_resp__(resp):
  if resp.status_code // 100 == 2: 
    return resp
  
  data = resp.json()
  if 'error' in data:
    msg = "%s: %s" % (data['error'], data['error_description'])
    logger.error(msg)
    raise Exception(msg)
  
  if isinstance(data, list):
    for error in data:
      if 'message' in error:
        msg = "%s: %s" % (error['errorCode'], error['message'])
        logger.error(msg)
        raise Exception(msg)

  msg = "request returned status code: %d" % resp.status_code
  logger.error(msg)
  raise Exception(msg)