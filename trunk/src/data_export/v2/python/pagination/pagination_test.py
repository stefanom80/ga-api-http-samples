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
"""Provides unit tests for pagination.py."""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import unittest
import pagination


class TestPaginator(unittest.TestCase):

  def testGetStartIndicies(self):
    page = pagination.Paginator(None, None)
    page.num_pages = 5
    page.start_index = 1
    indicies = page.GetStartIndicies()

    expected_indicies = [10001, 20001, 30001, 40001]
    self.assertEqual(expected_indicies, indicies)

    page.num_pages = 3
    page.start_index = 30001
    indicies = page.GetStartIndicies()

    expected_indicies = [40001, 50001]
    self.assertEqual(expected_indicies, indicies)

  def testDetermineNumPages(self):
    page = pagination.Paginator(None, None)
    page.max_pages = 10

    num_pages = page.DetermineNumPages(-1)
    self.assertEqual(10, num_pages)

    num_pages = page.DetermineNumPages(5)
    self.assertEqual(5, num_pages)

    num_pages = page.DetermineNumPages(11)
    self.assertEqual(10, num_pages)

    page.max_pages = 1
    num_pages = page.DetermineNumPages(-1)
    self.assertEqual(1, num_pages)

  def testGetIndexedTotalResults(self):
    page = pagination.Paginator(None, None)
    page.start_index = 1
    total_results = page.GetIndexedTotalResults('20000')
    self.assertEqual(20000, total_results)

    page.start_index = 10001
    total_results = page.GetIndexedTotalResults('30000')
    self.assertEquals(20000, total_results)

    page.start_index = 1001
    total_results = page.GetIndexedTotalResults('5000')
    self.assertEquals(4000, total_results)


  def testGetMaxPages(self):
    page = pagination.Paginator(None, None)
    page.start_index = 1
    page.total_results = 100000

    self.assertEqual(10, page.GetMaxPages())

    page.start_index = 10001
    page.total_results = page.GetIndexedTotalResults('100000')
    self.assertEquals(9, page.GetMaxPages())

    page.start_index = 1001
    page.total_results = page.GetIndexedTotalResults('5000')
    self.assertEquals(1, page.GetMaxPages())


if __name__ == '__main__':
  unittest.main()

