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
from act_sf_lookup import where_parser, lookup

class LookupTest(unittest.TestCase):

  def test_where_parser_phone(self):
    clause = where_parser("MobilePhone", "+14035695656")
    self.assertEqual("MobilePhone LIKE '%403%569%5656%'", clause)

  def test_where_parser_default(self):
    clause = where_parser("Name", "Alonso")
    self.assertEqual("Name='Alonso'", clause)    

  def test_where_parser_like(self):
    clause = where_parser("Name", "Alonso%")
    self.assertEqual("Name LIKE 'Alonso%'", clause)    

  def test_lookup_multi_where(self):
    sf = unittest.mock.Mock()
    sf.query.return_value = []

    lookup(sf, "Account", "Name", Name='Alonso', Postal="55555")

    _, req_kwargs = sf.query.call_args
    self.assertTrue(req_kwargs['query'] in [ 
        "SELECT Name FROM Account WHERE Name='Alonso' AND Postal='55555'",
        "SELECT Name FROM Account WHERE Postal='55555' AND Name='Alonso'"
        ])

  def test_lookup_count(self):
    sf = unittest.mock.Mock()
    sf.query.return_value = [{}]*200 # count = 200

    result = lookup(sf, "Account", "Name", Name='Alonso', Postal="55555")

    self.assertTrue('sf_count' in result)
    self.assertEqual(200, result['sf_count'])

  def test_lookup_empty(self):
    sf = unittest.mock.Mock()
    sf.query.return_value = []
    result = lookup(sf, "Account", "Name", Name='Alonso', Postal="55555")

    self.assertIsNotNone(result)


  
