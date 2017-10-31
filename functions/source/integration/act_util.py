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
from datetime import datetime, timedelta

logger = logging.getLogger()

def parse_date(value, date=datetime.now()):
    if "|" not in value:
        return value

    value_raw = value.split("|")
    delta_raw = value_raw[0].strip()
    format_raw = value_raw[1].strip()
    delta = timedelta()

    if format_raw not in formats:
      msg = "Supported formats are 'date', 'time' and 'datetime', example '2h|date'"
      logger.error(msg)
      raise Exception(msg)

    if len(delta_raw) > 0:
      delta_value = delta_raw[:-1] 
      delta_type = delta_raw[-1].lower()
      
      if delta_type not in timedeltas:
        msg = "Supported delta types are 'd' for days, 'h' for hours and 'm' for minutes, example '2h|date'"
        logger.error(msg)
        raise Exception(msg)
      
      delta = timedeltas[delta_type](delta_value)

    return (date+delta).strftime(formats[format_raw])

def split_bucket_key(location):
  bucketIndex = location.index('/')
  bucket = location[:bucketIndex]
  key = location[bucketIndex+1:]
  return (bucket, key)

def get_arg(kwargs, name):
  if name not in kwargs:
    msg = "'%s' enviroment variable is missing"
    logger.error(msg)
    raise Exception(msg)
  return kwargs[name]

formats = {
    "datetime":"%Y-%m-%dT%H:%M:%SZ",
    "date":"%Y-%m-%d",
    "time":"%H:%M:%S"
}

timedeltas = {
    "w":lambda v: timedelta(weeks=int(v)),
    "d":lambda v: timedelta(days=int(v)),
    "h":lambda v: timedelta(hours=int(v)),
    "m":lambda v: timedelta(minutes=int(v))
}
