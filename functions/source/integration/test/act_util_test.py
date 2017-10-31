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
from datetime import datetime
from act_util import get_arg, parse_date, split_bucket_key

class UtilTest(unittest.TestCase):

  def test_get_arg(self):
    env = {'KEY':1234}
    key = get_arg(env, "KEY")

    self.assertEqual(1234, key)

  def test_get_arg_not_present(self):
    with self.assertRaises(Exception):
      get_arg({}, "KEY")

  def test_parse_date_date(self):
    date = datetime(year=2017, month=12, day=24, hour=13, minute=45, second=59)
    self.assertEqual("2017-12-24", parse_date("|date", date))

  def test_parse_date_time(self):
    date = datetime(year=2017, month=12, day=24, hour=13, minute=45, second=59)
    self.assertEqual("13:45:59", parse_date("|time", date))  

  def test_parse_date_datetime(self):
    date = datetime(year=2017, month=12, day=24, hour=13, minute=45, second=59)
    self.assertEqual("2017-12-24T13:45:59Z", parse_date("|datetime", date))  

  def test_parse_date_delta_days(self):
    date = datetime(year=2017, month=12, day=24, hour=13, minute=45, second=59)
    self.assertEqual("2017-12-26", parse_date("2d|date", date))    

  def test_parse_date_delta_hours(self):
    date = datetime(year=2017, month=12, day=24, hour=13, minute=45, second=59)
    self.assertEqual("15:45:59", parse_date("2H|time", date))    

  def test_parse_date_delta_hours(self):
    date = datetime(year=2017, month=12, day=24, hour=13, minute=45, second=59)
    self.assertEqual("13:47:59", parse_date("2M|time", date))    

  def test_parse_date_delta_weeks(self):
    date = datetime(year=2017, month=12, day=20, hour=13, minute=45, second=59)
    self.assertEqual("2017-12-27", parse_date("1w|date", date))    

  def test_parse_date_delta_type_not_supported(self):
    date = datetime(year=2017, month=12, day=24, hour=13, minute=45, second=59)
    with self.assertRaises(Exception):
      parse_date("2q|date", date)

  def test_parse_date_delta_type_not_supported(self):
    date = datetime(year=2017, month=12, day=24, hour=13, minute=45, second=59)
    with self.assertRaises(Exception):
      parse_date("2d|bigdate", date)  

  def test_split_bucket_key_multi_folder(self):
    location = "connect-400eb9ae7f16/connect/asuarez-jul/CallRecordings/2017/07/13/2e2ec883-1145-4eb1-a8fd-0176911dcc95_20170713T13:47_UTC.wav"
    bucket, key = split_bucket_key(location)

    self.assertEqual("connect-400eb9ae7f16", bucket)
    self.assertEqual("connect/asuarez-jul/CallRecordings/2017/07/13/2e2ec883-1145-4eb1-a8fd-0176911dcc95_20170713T13:47_UTC.wav", key)

  def test_split_bucket_key_simple(self):
    bucket, key = split_bucket_key("my-bucket/file.txt")

    self.assertEqual("my-bucket", bucket)    
    self.assertEqual("file.txt", key)
