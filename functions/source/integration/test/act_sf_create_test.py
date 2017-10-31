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
from datetime import datetime
from act_sf_create import create

class CreateTest(unittest.TestCase):

  def test_create_multi_where(self):
    sf = unittest.mock.Mock()
    sf.create.return_value = "abc123"

    resp = create(sf, "Account", Name='Alonso', Postal="55555")

    self.assertTrue('Id' in resp)
    self.assertEqual("abc123", resp['Id'])

    _, req_kwargs = sf.create.call_args
    self.assertTrue('sobject' in req_kwargs)
    self.assertEqual("Account", req_kwargs['sobject'])
    self.assertTrue('data' in req_kwargs)
    data = req_kwargs['data']
    self.assertTrue('Name' in data)
    self.assertEqual("Alonso", data['Name'])
    self.assertTrue('Postal' in data)
    self.assertEqual("55555", data['Postal'])

  def test_create_with_date(self):
    sf = unittest.mock.Mock()
    sf.create.return_value = "abc123"

    resp = create(sf, "Account", Name='Alonso', CreateDate="|date")

    self.assertTrue('Id' in resp)
    self.assertEqual("abc123", resp['Id'])

    _, req_kwargs = sf.create.call_args
    self.assertTrue('sobject' in req_kwargs)
    self.assertEqual("Account", req_kwargs['sobject'])
    self.assertTrue('data' in req_kwargs)
    data = req_kwargs['data']
    self.assertTrue('Name' in data)
    self.assertEqual("Alonso", data['Name'])
    self.assertTrue('CreateDate' in data)
    date = datetime.strptime(data['CreateDate'], "%Y-%m-%d")
    self.assertAlmostEqual(datetime.now().year, date.year, delta=1)
    self.assertAlmostEqual(datetime.now().month, date.month, delta=1)
    self.assertAlmostEqual(datetime.now().day, date.day, delta=1)