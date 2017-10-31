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
import unittest.mock
from salesforce import Salesforce

class SalesforceTest(unittest.TestCase):

  def setUp(self):
    self.version = "v5" 
    self.consumer_key = "consumer_key"
    self.consumer_secret = "consumer_secret"
    self.username = "username" 
    self.password = "password"
    self.access_token = "access_token"

    self.sf = Salesforce(self.version, self.consumer_key,  self.consumer_secret, self.username, self.password)

  def test_sign_in(self):
    data = {'access_token':self.access_token, 'instance_url':'https://instanceid.salesforce.com'}
    resp = unittest.mock.Mock()
    resp.json.return_value = data
    self.sf.request = unittest.mock.Mock()    
    self.sf.request.post.return_value = resp
    
    self.sf.sign_in()

    self.assertEqual(data['access_token'], self.sf.access_token)
    self.assertEqual(data['instance_url'], self.sf.host)
    self.sf.request.post.called_once()
    _, kwargs = self.sf.request.post.call_args
    self.assertTrue("client_id" in kwargs['params']) 
    self.assertEqual(self.consumer_key, kwargs['params']['client_id'])
    self.assertTrue("client_secret" in kwargs['params'])
    self.assertEqual(self.consumer_secret, kwargs['params']['client_secret'])
    self.assertTrue("username" in kwargs['params'])
    self.assertEqual(self.username, kwargs['params']['username'])
    self.assertTrue(self.password in kwargs['params'])
    self.assertEqual(self.password, kwargs['params']['password'])
    self.assertTrue('Authorization' in self.sf.headers)
    self.assertTrue(self.sf.access_token in self.sf.headers['Authorization'])
    self.assertTrue("Content-Type" in self.sf.headers)
    self.assertEqual("application/json", self.sf.headers["Content-Type"])

  def test_query(self):
    self.sf.headers = { 
      'Authorization': 'Bearer %s' % self.access_token,
      'Content-Type': 'application/json'
    }
    self.sf.host = "https://instancid.salesforce.com"
    data_original = {"done":True,"totalSize":2,"records":[{"attributes":{"type":"Account","url":"/services/data/v20.0/sobjects/Account/001D000000IRFmaIAH"},"Name":"Test 1"},{"attributes":{"type":"Account","url":"/services/data/v20.0/sobjects/Account/001D000000IomazIAB"},"Name":"Test 2"}]}
    resp = unittest.mock.Mock()
    resp.json.return_value = data_original
    self.sf.request.get = unittest.mock.Mock(return_value=resp)

    query = "SELECT Name FROM Account"
    data = self.sf.query(query)

    self.assertEqual(data_original['records'], data)
    _, kwargs = self.sf.request.get.call_args
    self.assertEqual(self.sf.host+"/services/data/"+self.version+"/query", kwargs['url'])
    self.assertTrue('params' in kwargs)
    self.assertEqual(query, kwargs['params']['q'])
    
  def test_search(self):
    self.sf.headers = { 
      'Authorization': 'Bearer %s' % self.access_token,
      'Content-Type': 'application/json'
    }
    self.sf.host = "https://instancid.salesforce.com"
    data_original = {"searchRecords":[{"attributes":{"type":"Account","url":"/services/data/v35.0/sobjects/Account/001D000000IqhSLIAZ"},"Id":"001D000000IqhSLIAZ",},{"attributes":{"type":"Account","url":"/services/data/v35.0/sobjects/Account/001D000000IomazIAB"},"Id":"001D000000IomazIAB"}]}
    resp = unittest.mock.Mock()
    resp.json.return_value = data_original
    self.sf.request.get = unittest.mock.Mock(return_value=resp)

    query = "FIND Acme"
    data = self.sf.search(query)

    self.assertEqual(data_original['searchRecords'], data)
    _, kwargs = self.sf.request.get.call_args
    self.assertEqual(self.sf.host+"/services/data/"+self.version+"/search", kwargs['url'])
    self.assertTrue('params' in kwargs)
    self.assertEqual(query, kwargs['params']['q'])

  def test_update(self):
    self.sf.headers = { 
      'Authorization': 'Bearer %s' % self.access_token,
      'Content-Type': 'application/json'
    }
    self.sf.host = "https://instancid.salesforce.com"
    self.sf.request = unittest.mock.Mock(return_value=(None, None))
    
    sobject = "Case"
    data = {'Name': 'Pete'}
    sojb_id = "abc"
    self.sf.update(sobject, sojb_id, data)

    _, kwargs = self.sf.request.patch.call_args
    self.assertEqual(self.sf.host+"/services/data/v5/sobjects/Case/abc", kwargs['url'])
    self.assertEqual(data, kwargs['data']) 
    self.assertEqual(self.sf.headers, kwargs['headers'])
    
  def test_update_by_external(self):
    self.sf.headers = { 
      'Authorization': 'Bearer %s' % self.access_token,
      'Content-Type': 'application/json'
    }
    self.sf.host = "https://instancid.salesforce.com"
    self.sf.request = unittest.mock.Mock(return_value=None)
    
    sobject = "Case"
    sfield = "call_id__c"
    data = {'Name': 'Pete'}
    sojb_id = "abc"
    self.sf.update_by_external(sobject, sfield, sojb_id, data)

    _, kwargs = self.sf.request.patch.call_args
    self.assertEqual(self.sf.host+"/services/data/v5/sobjects/Case/call_id__c/abc", kwargs['url'])
    self.assertEqual(data, kwargs['data']) 
    self.assertEqual(self.sf.headers, kwargs['headers'])
    

  def test_create(self):
    self.sf.headers = { 
      'Authorization': 'Bearer %s' % self.access_token,
      'Content-Type': 'application/json'
    }
    self.sf.host = "https://instancid.salesforce.com"
    resp_data = {"id":"001D000000IqhSLIAZ","errors":[],"success":True}
    resp = unittest.mock.Mock()
    resp.json.return_value = resp_data
    self.sf.request.post = unittest.mock.Mock(return_value=resp)
    
    sobj = "Account"
    data = {'Name': 'Pete'}
    new_id = self.sf.create(sobj, data)

    self.assertEqual(resp_data['id'], new_id)
    _, kwargs = self.sf.request.post.call_args
    self.assertTrue('url' in kwargs)
    self.assertEqual(self.sf.host+"/services/data/v5/sobjects/Account", kwargs['url'])
    self.assertTrue('data' in kwargs)
    self.assertEqual(data, kwargs['data'])
    self.assertEqual(self.sf.headers, kwargs['headers'])

  def test_delete(self):
    self.sf.headers = { 
      'Authorization': 'Bearer %s' % self.access_token,
      'Content-Type': 'application/json'
    }
    self.sf.host = "https://instancid.salesforce.com"
    resp = unittest.mock.Mock()
    resp.json.return_value = "create_data"
    self.sf.request.delete = unittest.mock.Mock(return_value=resp)
    
    sobj = "Account"
    sobj_id = "abc"
    self.sf.delete(sobj, sobj_id)

    _, kwargs = self.sf.request.delete.call_args
    self.assertTrue('url' in kwargs)
    self.assertEqual(self.sf.host+"/services/data/v5/sobjects/Account/abc", kwargs['url'])
    self.assertEqual(self.sf.headers, kwargs['headers'])


  def test_set_production(self):
    current_login_host = self.sf.login_host 
    self.sf.set_production()

    self.assertNotEqual(current_login_host, self.sf.login_host)

  @unittest.skip("Configuration required")
  def test_end_to_end(self):
    import os
    import sf_config
    import uuid
    sf = Salesforce(version=os.environ["SF_VERSION"], 
      consumer_key=os.environ["SF_CONSUMER_KEY"], 
      consumer_secret=os.environ["SF_CONSUMER_SECRET"], 
      username=os.environ["SF_USERNAME"], 
      password=os.environ["SF_PASSWORD"]) 
    sf.sign_in()
    name = str(uuid.uuid4())
    sf.create("Account", {'Name': name})
    acc = sf.query("SELECT Id FROM Account WHERE Name='%s'" % name)[0]
    sf.update("Account", sobj_id=acc['Id'], data={"Description":"hello world"})
    sf.delete("Account", acc['Id'])


