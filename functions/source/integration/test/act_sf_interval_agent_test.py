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
import unittest, datetime
from act_sf_interval_agent import prepare_agent_record, label_parser, value_parser

class AgentInterval(unittest.TestCase):
  def test_prepare_agent_record_id(self):
    record_raw = {'Agent':'Alonso'}
    record = prepare_agent_record(record_raw, "20171115")

    self.assertTrue("report_id__c" in record, "report_id__c not present")
    self.assertEqual("Alonso20171115", record['report_id__c'])

  def test_prepare_agent_record_name(self):
    record_raw = {'Agent':'Alonso'}
    record = prepare_agent_record(record_raw, "20171115")

    self.assertTrue("ac_object_name__c" in record)
    self.assertEqual("Alonso", record['ac_object_name__c'])

  def test_prepare_agent_record_type(self):
    record_raw = {'Agent':'Alonso'}
    record = prepare_agent_record(record_raw, "20171115")

    self.assertTrue("type__c" in record)
    self.assertEqual("Agent", record["type__c"])

  def test_label_parser(self):
    self.assertEqual("average__c", label_parser("Average"))

  def test_label_parser_with_fix(self):
    self.assertEqual("avg_agent_interaction_and_cust_hold_time__c", label_parser("Average Agent Interaction And Customer Hold Time"))

  def test_label_parser_object_name(self):
    self.assertEqual("ac_object_name__c", label_parser("Agent"))

  def test_value_parser(self):
    self.assertIsNone(value_parser(""))

  def test_value_parser_with_percent(self):
    self.assertEqual("0.00", value_parser("0.00%"))    
