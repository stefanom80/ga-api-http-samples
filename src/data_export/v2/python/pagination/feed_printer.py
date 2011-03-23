#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility to convert a Data Export API feed into TSV.

This provides utitlites to both print TSV files to the standard output
as well as directly to a file.

  GetTsvFilePrinter: Returns an instantiated object to output to files.
  GetTsvScreenPrinter: Returns an instantiated object to output to the screen.
  UnicodeWriter(): Utf-8 encodes output.
  FeedPrinter(): Converts the Data Export API response into tabular data.
"""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import codecs
import cStringIO
import csv
import sys


def GetTsvFilePrinter(file_name):
  """Returns a Feed Printer object to output to file_name.

  Args:
    file_name: string The name of the file to output to.

  Returns:
    The newly created FeedPrinter object.
  """
  my_handle = open(file_name, 'wb')
  writer = UnicodeWriter(my_handle, dialect='excel-tab')
  return FeedPrinter(writer)


def GetTsvScreenPrinter():
  """Returns a Feed Printer object to output to std.stdout."""
  writer = UnicodeWriter(sys.stdout, dialect='excel-tab')
  return FeedPrinter(writer)


# Wrapper to output to utf-8. Taken mostly / directly from Python docs:
# http://docs.python.org/library/csv.html
class UnicodeWriter(object):
  """A CSV writer which uses the csv module to output csv compatible formats.

  Will write rows to CSV file "f", which is encoded in the given encoding.
  """

  def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
    # Redirect output to a queue
    self.queue = cStringIO.StringIO()
    self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
    self.stream = f
    self.encoder = codecs.getincrementalencoder(encoding)()

  def writerow(self, row):
    self.writer.writerow([s.encode('utf-8') for s in row])
    # Fetch UTF-8 output from the queue ...
    data = self.queue.getvalue()
    data = data.decode('utf-8')
    # ... and reencode it into the target encoding
    data = self.encoder.encode(data)
    # write to the target stream
    self.stream.write(data)
    # empty queue
    self.queue.truncate(0)

  def writerows(self, rows):
    for row in rows:
      self.writerow(row)


class FeedPrinter(object):
  """Utility class to output a the data feed as tabular data."""

  def __init__(self, writer):
    """Initializes the class.

    Args:
      writer: An instance of UnicodeWriter.
    """
    self.writer = writer

  def Output(self, feed):
    """Outputs rows of data retrieved from the Data Export API.

    This uses the csv_writer object to output the dimension and metrics names
    as well as all the values in the feed.

    Args:
      feed: gdata.analytics.data.DataFeed The feed to output.
    """
    # Write the headers.
    if feed and feed.entry:
      row = []
      for dim in feed.entry[0].dimension:
        row.append(dim.name)
      for met in feed.entry[0].metric:
        row.append(met.name)
      self.writer.writerow(row)

    # Write the data.
    for entry in feed.entry:
      row = []
      for dim in entry.dimension:
        row.append(dim.value)
      for met in entry.metric:
        row.append(met.value)
      self.writer.writerow(row)


